#!/usr/bin/env python3
"""regenerate-hints.py — Derive repair-hints.json from current audit results.

For every non-PASS program (COMPILE_FAIL, BUILD_FAIL, RUN_FAIL, SEGFAULT,
WRONG_OUTPUT, NO_TEST_CASE), produce one or more targeted hints based on:

  - the program's status (compile/build/run/output)
  - every error_code present (not just the first) — programs may need
    multiple fixes (e.g. E1003 square brackets AND E1004 unterminated string)
  - the detailed message + got/expected fields where useful (e.g. specific
    "starts with keyword 'as'" vs "is not declared")
  - presence of "CODE IS TRUNCATED" signals (source < 50b, refusal text,
    "end of file" errors)

Output: results/repair-hints.json overwritten with one entry per non-PASS
program. Schema preserved: {pid: {status: ..., hints: [str, ...]}}.

Run from toke-test-programs root after a fresh local-audit.py:
  python3 infra/regenerate-hints.py
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "results" / "audit-report.json"
HINTS = ROOT / "results" / "repair-hints.json"
SOLUTIONS = ROOT / "results" / "solutions"
HELD   = ROOT / "results" / "held-programs.json"


def load_held_lookup() -> dict[str, str]:
    """Return {pid: reason} for programs on hold pending Python-ref repair."""
    if not HELD.exists():
        return {}
    try:
        data = json.loads(HELD.read_text())
        return {p["id"]: p.get("reason", "unknown") for p in data.get("programs", [])}
    except (json.JSONDecodeError, OSError, KeyError):
        return {}

# ── refusal/stub detection ──────────────────────────────────────────────
REFUSAL_PHRASES = (
    "i'm sorry", "i am sorry", "i cannot", "i can't",
    "i am not able", "i'm not able", "as an ai", "i do not assist",
)


def is_refusal_or_stub(category: str, pid: str, source_bytes: int) -> bool:
    if source_bytes < 50:
        return True
    sol = SOLUTIONS / category / pid / "solution.tk"
    if not sol.exists():
        return True
    try:
        head = sol.read_text(errors="replace")[:200].lower()
    except OSError:
        return False
    return any(p in head for p in REFUSAL_PHRASES)


# ── per-error-code hint generators ─────────────────────────────────────
def hint_e1001(d: dict) -> str:
    return ("Invalid escape sequence in string literal. Toke string escapes: "
            r'\" \\ \n \t \r \0 \xNN. Nothing else after \\.')


def hint_e1003(d: dict) -> str:
    msg = d.get("message", "")
    got = d.get("got", "")
    if "square brackets" in msg:
        return ("Square brackets not allowed. Use @(item1;item2;item3) for arrays "
                "and maps; arr.get(idx) for access; arr.len for length.")
    if "underscore" in msg:
        return ("Identifier contains underscore (v0.2 syntax). Concatenate words: "
                "my_var → myvar, to_int → toint, get_count → getcount.")
    if "character outside" in msg or got == "\\":
        return ("Character outside the toke alphabet. Only lowercase a-z, digits 0-9, "
                "and toke operators allowed. Common causes: uppercase letters, "
                "underscores, or stray backslashes inside string literals "
                r'(use \" exactly once per embedded quote — never JSON-style triple-escape).')
    return "Lexical error E1003. Check identifier and string contents conform to the toke alphabet."


def hint_e1004(d: dict) -> str:
    return ("Unterminated string literal at end of file. Every \" needs a closing \". "
            "If the program looks truncated, regenerate from scratch.")


def hint_e2001(d: dict) -> str:
    return ("Token-level parse error. Check the first ~50 chars — model may have "
            "written non-toke (JSON, markdown, plain English). Programs must start "
            "with m=name;")


def hint_e2002(d: dict) -> str:
    got = d.get("got", "").strip("'\"")
    if got == "el":
        return ("'el' must directly follow an if(...){...} block: "
                "if(cond){body}el{body}. Cannot stand alone.")
    if got == ")":
        return ("Extra closing paren ')'. Count parens — every '(' needs exactly one ')'. "
                "Common cause: doubled if((cond)) or trailing paren on a call.")
    if got == "{":
        return ("Unexpected '{'. Blocks may only follow if/el/lp, function or type bodies. "
                "Check whether a previous statement is missing its ;.")
    if got == "}":
        return ("Unexpected '}'. A block closed early — usually a missing ; before this } "
                "or an extra } from over-nesting.")
    return ("Unexpected token in expression. Common causes: (a) keyword used as identifier "
            "(i, f, t, m, as, el, lp, br, let, mut, rt, mt) — rename; "
            "(b) missing operator between values; "
            "(c) comma instead of semicolon (toke uses ; everywhere).")


def hint_e2003(d: dict) -> str:
    return ("Missing semicolon. Toke separates EVERY statement with ; (never newlines). "
            "Every let/assignment/call/return needs a trailing ;. Inside lp(){body}, "
            "body statements also need ; between them.")


def hint_e2004(d: dict) -> str:
    msg = d.get("message", "")
    got = d.get("got", "")
    if "match" in msg:
        return ("'match' is not a toke keyword. Use 'mt' instead: "
                "mt(expr){|case1;result1|case2;result2}.")
    if got == "end of file" or "end of file" in msg or "unclosed delimiter" in msg:
        return ("Code is incomplete — truncated or an unclosed (/[/{/\". "
                "Count opening vs closing delimiters; if the program looks heavily "
                "truncated, rewrite the complete program from scratch rather than "
                "trying to patch the end.")
    return "Unexpected end of file or unclosed delimiter. Add the missing closing token."


def hint_e2005(d: dict) -> str:
    return ("Unexpected token in type position. Expected a type after ':' — "
            "scalar ($i64, $f64, $str, $bool, $void), struct ($name), "
            "array (@($t)), or function type (($t):$r). Type names need $ prefix; "
            "no uppercase, no underscores.")


def hint_e2030(d: dict) -> str:
    return ("Parse error E2030. Often indicates a structural rule violation — "
            "check that m=name; comes first, then i= imports, then t= types, "
            "then f= functions.")


def hint_e3011(d: dict) -> str:
    msg = d.get("message", "")
    m = re.search(r"identifier '([^']+)' starts with keyword '([^']+)'", msg)
    if m:
        ident, kw = m.group(1), m.group(2)
        return (f"Identifier '{ident}' starts with keyword '{kw}'. Rename — toke's "
                f"parser tokenises the keyword first, causing cascading errors. "
                f"Use a/b/c/x/y/n or full distinct words like idx, count, value.")
    m = re.search(r"identifier '([^']+)' is not declared", msg)
    if m:
        ident = m.group(1)
        fix = d.get("fix", "")
        suggestion = ""
        ms = re.search(r"did you mean '([^']+)'", fix)
        if ms:
            suggestion = f" Did you mean '{ms.group(1)}'?"
        return (f"Undeclared identifier '{ident}'. Check spelling; ensure it is "
                f"bound with let before use; verify imports.{suggestion}")
    return "Identifier resolution error E3011. Check spelling, bindings, and imports."


def hint_e4031(d: dict) -> str:
    expected = d.get("expected", "")
    got = d.get("got", "")
    if expected and expected == got:
        # The str+str bug — surface the v0.3.x design + canonical fix
        return ("Type mismatch with identical types on both sides — "
                "this usually means '+' was used on strings. In toke v0.3.x, "
                "`+` is numeric-only. For string templates use interpolation: "
                r'"\(a)\(b)". For variadic concat: s.concat(a;b;c). '
                "For collections: s.join(arr;sep). For dynamic accumulators: s.builder().")
    if expected and got:
        return (f"Type mismatch: expected {expected}, got {got}. "
                f"Cast with 'as' if conversion is intended (e.g. n as $str), "
                f"or fix the producer expression.")
    return "Type mismatch E4031. Check declared vs actual types on the failing expression."


def hint_e4070(d: dict) -> str:
    msg = d.get("message", "")
    m = re.search(r"binding '([^']+)'", msg)
    name = m.group(1) if m else "the binding"
    return (f"Cannot reassign immutable binding '{name}'. Change `let {name}=...` "
            f"to `let {name}=mut....`. CRITICAL: scan the ENTIRE function for "
            f"every other `let X=` that is reassigned later (X=expr) and convert "
            f"them ALL to `let X=mut....` in ONE edit. Doing this one at a time "
            f"wastes repair iterations.")


def hint_e5001(d: dict) -> str:
    return ("Value escapes its scope. Returning a string/array/struct from a "
            "nested block is now safe (heap-allocated, 110.7 fix). For i64/f64 "
            "locals from nested blocks, move the binding to the function body "
            "or wrap the return path differently.")


def hint_e5002(d: dict) -> str:
    return "Arena error E5002. Check memory ownership / lifetime of the flagged value."


def hint_e9020(d: dict) -> str:
    return ("E9020: no main function defined. Every EXECUTABLE toke program "
            "needs an entry point. Add `f=main():$i64{<0}` (or a body that "
            "reads stdin via io.readln() / calls your helpers / prints with "
            "io.println() / returns <0). Library-shape modules with no main "
            "compile under --check but cannot be linked into an executable "
            "binary.")


# ── W-series warnings that the diag layer reports as errors in some configs ──
def hint_w1010(d: dict) -> str:
    return ('String interpolation "\\(expr)" used. In v0.3.x this becomes the canonical '
            'pattern for templates. Make sure the interpolated expression is $str — '
            'use s.fromint(n) for ints, s.format(f;"%.4f") for floats.')


def hint_w1020(d: dict) -> str:
    return ("Foreign-language keyword detected. Toke does not have this keyword. "
            "Check the toke keyword list (m f t i if el lp br let mut as rt mt) and "
            "rewrite using a toke equivalent.")


def hint_w2020(d: dict) -> str:
    # Same case as the E3011 starts-with-keyword branch — W2020 is the parser's
    # warning that the type-checker later upgrades to E3011/E4070 cascades.
    msg = d.get("message", "")
    m = re.search(r"identifier '([^']+)' starts with keyword '([^']+)'", msg)
    if m:
        ident, kw = m.group(1), m.group(2)
        return (f"Identifier '{ident}' starts with keyword '{kw}'. Rename to avoid "
                f"the W2020 → E3011/E4070 cascade. Use a/b/c/x/y/n or full words "
                f"like idx, count, value — never start an identifier with as, el, "
                f"lp, br, mt, rt, mut, let, if.")
    return ("W2020 keyword-prefix warning. Identifier collides with a keyword's "
            "leading characters. Rename to a distinct word.")


def hint_w5001(d: dict) -> str:
    # 110.7 already suppresses the false-positive cases (TY_STR/ARRAY/STRUCT/UNKNOWN)
    return ("W5001 escape-scope warning still firing — value type is a stack-allocated "
            "primitive ($i64/$f64/$bool). Move the binding to the function body, "
            "or restructure so the value is returned from the outer scope.")


def hint_e9003(d: dict) -> str:
    return ("E9003: clang invocation failed during LLVM IR → binary linking. "
            "Generated IR is syntactically valid for tkc but rejected by clang. "
            "Common causes: stdlib glue mismatch (function arity/types differ "
            "between declaration and definition); calling a function not in the "
            "loaded stdlib subset; ABI mismatch (i64 vs i32 vs f64 return type). "
            "Check the clang stderr for the specific symbol or type error and "
            "align the toke source with the stdlib signature.")


def hint_build_fail(extra: dict) -> str:
    # If E9020 (missing main) is in the codes, surface its specific hint —
    # the linker error dominates the rest of the build output.
    codes = extra.get("error_codes") or []
    if "E9020" in codes:
        return ("E9020: no main function defined. Every EXECUTABLE toke program "
                "needs an entry point. Add `f=main():$i64{<0;}` (or one that "
                "reads stdin via io.readln(), calls your helper functions, and "
                "prints results via io.println). Library-only modules compile "
                "under --check but cannot be built into a runnable binary.")
    return ("Build (link) failed — usually a missing stdlib glue function. "
            "Stick to std.io, std.str, std.math, std.json, std.file, std.time, "
            "std.env, std.process. AVOID: std.auth, std.canvas, std.chart, "
            "std.dashboard, std.dataframe, std.svg, std.html, std.analytics, "
            "std.ml, std.image, std.zip — these are declared but not implemented.")


def hint_run_fail(extra: dict) -> str:
    return ("Runtime failure. Check stderr (in attempts/<id>/iter-N.error.txt) "
            "for the actual cause. Common: RT002 (integer overflow — use $f64 "
            "for large math), division by zero, OOB array access.")


def hint_segfault(extra: dict) -> str:
    return ("Segfault. Almost always a null/OOB access: arr.get(idx) on empty array, "
            "s.slice() with out-of-range indices, struct field on uninitialised pointer. "
            "Add `if(arr.len > 0)` / `if(idx < arr.len)` guards before every .get(); "
            "verify nullable values before use.")


def hint_wrong_output(extra: dict) -> str:
    return ("Compiles + builds + runs, but output doesn't match expected. "
            "Verify: (a) format strings — use s.format(val;\"%.4f\") for floats "
            "with exact decimal places; (b) trailing newlines / whitespace match "
            "the expected output exactly; (c) loop boundaries (off-by-one); "
            "(d) algorithm correctness against the test cases.")


def hint_timeout(extra: dict) -> str:
    return ("Execution timed out. Loop may be infinite or O(N²+) on large input. "
            "Check loop termination condition; avoid string += in tight loops "
            "(use s.builder() in v0.3.x); ensure recursion has a base case.")


def hint_no_test_case(extra: dict) -> str:
    return ("Requirement has no test_cases defined. Either add test_cases with "
            "input/expected_output, or mark the requirement as documentation-only.")


CODE_HANDLERS = {
    "E1001": hint_e1001,
    "E1003": hint_e1003,
    "E1004": hint_e1004,
    "E2001": hint_e2001,
    "E2002": hint_e2002,
    "E2003": hint_e2003,
    "E2004": hint_e2004,
    "E2005": hint_e2005,
    "E2030": hint_e2030,
    "E3011": hint_e3011,
    "E4031": hint_e4031,
    "E4070": hint_e4070,
    "E5001": hint_e5001,
    "E5002": hint_e5002,
    "E9003": hint_e9003,
    "E9020": hint_e9020,
    "W1010": hint_w1010,
    "W1020": hint_w1020,
    "W2020": hint_w2020,
    "W5001": hint_w5001,
}

STATUS_HANDLERS = {
    "BUILD_FAIL":   hint_build_fail,
    "RUN_FAIL":     hint_run_fail,
    "SEGFAULT":     hint_segfault,
    "WRONG_OUTPUT": hint_wrong_output,
    "TIMEOUT":      hint_timeout,
    "NO_TEST_CASE": hint_no_test_case,
}


def derive_hints(prog: dict) -> list[str]:
    """Return a list of unique, ordered hints for a single program."""
    status = prog.get("status", "")
    if status == "PASS":
        return []

    hints: list[str] = []
    seen: set[str] = set()

    def add(h: str) -> None:
        if h and h not in seen:
            seen.add(h)
            hints.append(h)

    # Truncated-stub or refusal — most useful single hint
    if is_refusal_or_stub(prog.get("category", ""), prog["id"],
                          prog.get("source_bytes", 0)):
        add("No real toke source on disk (refusal text or truncated stub). "
            "Regenerate the complete program from scratch — do not try to "
            "incrementally fix what's there.")

    # COMPILE_FAIL: walk every diagnostic and emit one hint per distinct error code
    if status == "COMPILE_FAIL":
        emitted_codes: set[str] = set()
        raw = prog.get("error", "")
        for line in raw.split("\n"):
            if not line.strip():
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            code = d.get("error_code", "")
            if code in emitted_codes:
                continue
            h = CODE_HANDLERS.get(code, lambda _d: None)(d)
            if h:
                add(h)
                emitted_codes.add(code)
        if not hints:
            add(f"Compile failed with no specific code matcher. Inspect "
                f"results/audit-report.json entry for {prog['id']} for raw diagnostics.")

    # BUILD_FAIL / RUN_FAIL / SEGFAULT / WRONG_OUTPUT / TIMEOUT / NO_TEST_CASE
    handler = STATUS_HANDLERS.get(status)
    if handler:
        add(handler(prog))

    return hints


def main() -> None:
    if not AUDIT.exists():
        raise SystemExit(f"missing {AUDIT}; run infra/local-audit.py first")
    audit = json.loads(AUDIT.read_text())
    programs = audit.get("programs", [])
    held = load_held_lookup()

    out: dict = {}
    stats = defaultdict(int)
    for p in programs:
        pid = p["id"]
        status = p.get("status", "")
        if pid in held:
            # Held programs get a single explicit hint so any repair loop
            # that does pick them up knows not to spend credit.
            out[pid] = {
                "status": status,
                "held": True,
                "hold_reason": held[pid],
                "hints": [
                    "ON HOLD — the Python reference for this program is broken "
                    f"({held[pid]}). Skip toke repair until the Python ref is fixed "
                    "(story Epic 107 follow-up). See results/held-programs.json."
                ],
            }
            stats[f"held_{held[pid]}"] += 1
            continue
        if status == "PASS":
            continue
        hints = derive_hints(p)
        if not hints:
            stats["no_hint"] += 1
            continue
        out[pid] = {"status": status, "hints": hints}
        stats[f"hinted_{status}"] += 1
        stats[f"hint_count_{len(hints)}"] += 1

    HINTS.write_text(json.dumps(out, indent=2, sort_keys=True))
    print(f"wrote {len(out)} hint entries to {HINTS}")
    print("breakdown:")
    for k, n in sorted(stats.items()):
        print(f"  {k}: {n}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""worker-generate.py — Main generation script for toke worker instances.

Reads requirements from categories/*/requirements.yaml, partitions work across
workers by hash, generates solutions via api.tokelang.dev, and repairs failures
using the Anthropic API (Claude).

Stateless/resumable: progress tracked in /opt/toke-worker/state.json.
"""

import hashlib
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

# --- Configuration ---
WORKER_ID = int(os.environ.get("WORKER_ID", "1"))
TOTAL_WORKERS = int(os.environ.get("TOTAL_WORKERS", "5"))
TOKE_API_URL = os.environ.get("TOKE_API_URL", "https://api.tokelang.dev")
TOKE_API_KEY = os.environ.get("TOKE_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# 107.R4.1: DRY_RUN=1 stubs Anthropic + toke API calls + isolates state to
# state-dryrun.json / budget-dryrun.json so we can validate the manifest +
# prompt-format + compile/test pipeline locally without spending any API.
DRY_RUN = os.environ.get("DRY_RUN", "").lower() in ("1", "true", "yes")
WORKER_DIR_OVERRIDE = os.environ.get("WORKER_DIR")  # for local testing

WORKER_DIR = Path(WORKER_DIR_OVERRIDE) if WORKER_DIR_OVERRIDE else Path("/opt/toke-worker")
REPOS_DIR = WORKER_DIR / "repos"
TEST_PROGRAMS_DIR = REPOS_DIR / "toke-test-programs"
LOGS_DIR = WORKER_DIR / "logs"
SOLUTIONS_DIR = WORKER_DIR / "solutions"
FAILED_DIR = WORKER_DIR / "failed"
# Separate state + budget files when DRY_RUN so we don't clobber real runs.
STATE_FILE = WORKER_DIR / ("state-dryrun.json" if DRY_RUN else "state.json")
BUDGET_FILE = WORKER_DIR / ("budget-dryrun.json" if DRY_RUN else "budget.json")

MAX_SONNET_ITERATIONS = int(os.environ.get("MAX_SONNET_ITERATIONS", "10"))
MAX_OPUS_ITERATIONS = int(os.environ.get("MAX_OPUS_ITERATIONS", "5"))
MAX_REPAIR_ITERATIONS = MAX_SONNET_ITERATIONS + MAX_OPUS_ITERATIONS
BUDGET_USD_CAP = float(os.environ.get("BUDGET_USD_CAP", "20.0"))
USE_TOKE_API = os.environ.get("USE_TOKE_API", "1").lower() not in ("0", "false", "no")
RUN_MODE = os.environ.get("RUN_MODE", "baseline")
MANIFEST_PATH = os.environ.get("MANIFEST_PATH", "")
RATE_LIMIT_DELAY = 1.0
TKC_TIMEOUT = 60
TEST_TIMEOUT = 10
BUILD_COOLDOWN = 2.0
# Per-1M-token pricing for budget tracking (Anthropic public list, USD).
PRICE_PER_MTOK = {
    "sonnet": {"input": 3.00,  "output": 15.00},
    "opus":   {"input": 15.00, "output": 75.00},
}
# 107.R2: per-program override (max_sonnet/max_opus/model from manifest)
PROGRAM_OVERRIDES: dict[str, dict] = {}

# --- Logging ---
LOGS_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / f"worker-{WORKER_ID}.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

# --- Toke system prompt for repair ---
TOKE_SYSTEM_PROMPT = """You write toke programs. toke is a compiled language with a 55-char alphabet.

STRUCTURE: m=name; then i=alias:std.module; then f= and t= declarations.
KEYWORDS (13): m f t i if el lp br let mut as rt mt

SYNTAX RULES:
- Semicolons separate ALL statements AND function parameters. NEVER use commas.
- No square brackets. Arrays: @(1;2;3). Access: arr.get(idx). Length: arr.len() or arr.len
- Functions: f=name(p1:$i64;p2:$str):$i64{body}
- Return: <expr; (preferred) or rt expr;
- Loops: lp(let idx=0;idx<=n;idx=idx+1){body} or lp(condition){body}
- MUTABLE variables: let x=mut.0; then x=x+1; — WITHOUT mut. you CANNOT reassign.
  WRONG: let x=0; x=x+1;  — this is E4070 error
  RIGHT: let x=mut.0; x=x+1;
- Mutable strings: let s=mut.""; s=s+"more";
- Mutable floats: let x=mut.0.0; x=x+1.0;
- Types: $i64 $f64 $str $bool $void — ALL need $ prefix.
- Comparison: = (equals) < > <= >= != — all supported.
- Module: m=name; (FIRST line, always. Use lowercase, no special chars.)
- Import: i=alias:std.module; then alias.func()
- NEVER use i/f/t/m as variable names — they are keywords.
- No 'return'/'fn'/'func'/'for'/'while'/'else'/'int'/'string' — NOT toke keywords.

STDLIB FUNCTIONS (use via import alias):
  i=io:std.io    → io.readln():$str  io.println(val)  io.eprintln(val)
  i=s:std.str    → s.toint(str):$i64  s.fromint(n):$str  s.tofloat(str):$f64  s.fromfloat(f):$str
                   s.len(str):$i64  s.split(str;sep):array  s.concat(a;b):$str
                   s.trim(str):$str  s.slice(str;start;end):$str  s.contains(str;sub):$bool
                   s.format(val;fmt):$str  (e.g. s.format(3.14;"%.2f"))
  i=math:std.math → math.sqrt(f):$f64  math.pow(base;exp):$f64  math.abs(n):$i64
                    math.sin(f):$f64  math.cos(f):$f64  math.ln(f):$f64  math.log10(f):$f64

NULL SAFETY: Always check split results before accessing:
  let parts=s.split(line;" ");
  if(parts.len()>=2){let second=parts.get(1)};  — check length BEFORE get

WORKING EXAMPLES:

Factorial (recursion + readln + toint):
m=fact;i=io:std.io;i=s:std.str;f=fact(n:$i64):$i64{if(n<2){<1};<n*fact(n-1)};f=main():$i64{let line=io.readln();let n=s.toint(line);io.println(s.fromint(fact(n)));<0}

Sum 1 to N (mutable + while loop + <=):
m=sum;i=io:std.io;i=s:std.str;f=main():$i64{let n=s.toint(io.readln());let total=mut.0;let idx=mut.1;lp(idx<=n){total=total+idx;idx=idx+1};io.println(s.fromint(total));<0}

Split + parse (string processing):
m=parse;i=io:std.io;i=s:std.str;f=main():$i64{let line=io.readln();let parts=s.split(line;" ");if(parts.len()>=2){let a=s.toint(parts.get(0));let b=s.toint(parts.get(1));io.println(s.fromint(a+b))}el{io.println("error")};<0}

Float math:
m=calc;i=io:std.io;i=s:std.str;i=math:std.math;f=main():$i64{let x=s.tofloat(io.readln());let result=math.sqrt(x);io.println(s.fromfloat(result));<0}

Output ONLY toke source code. No explanation. No markdown."""

TOKE_REPAIR_PROMPT = """Fix this toke program. Address the SPECIFIC error shown.

REQUIREMENT: {description}

ALL TEST CASES (your program must pass EVERY one):
{all_test_cases_block}
{program_hints}
CURRENT SOURCE:
```toke
{source}
```

ERROR:
{error}

COMMON FIXES:
- E4070 "cannot assign to immutable": Change `let x=0` to `let x=mut.0` for ANY variable you reassign later. EVERY variable that gets x=x+1 or x=newval MUST use mut.
- E2002 parse error: Check for commas (use semicolons), missing semicolons between statements, wrong keywords (fn→f=, for→lp, else→el, return→<). If you see 10+ E2002s in a cascade, fix only the FIRST one — the rest are usually downstream noise.
- E1003 illegal char: Remove uppercase letters, underscores in identifiers, or characters outside a-z 0-9 and the 19 allowed symbols.
- E9003 clang link failure: Stdlib glue mismatch — function arity/types differ. Re-check signatures (e.g. s.split takes 2 args, separated by `;`).
- Segfault/crash: Check array bounds before .get(). Check that split result has enough elements. Avoid chaining operations on potentially null values.
- Wrong output: Check algorithm logic. Verify integer vs float types ($i64 vs $f64). Check that io.println outputs the right format.
- "undefined reference": Use the import alias (s.toint not str.toint). Check function exists in stdlib.
- "undefined reference to main": You forgot to define `f=main():$i64{{...<0}}`. The build step needs this entry point; library-only programs cannot link. (E9003)

KEY PATTERNS:
- Mutable: let x=mut.0; let s=mut.""; let arr=mut.@();
- Read+parse: let n=s.toint(io.readln());
- Split safely: let parts=s.split(line;" "); if(parts.len()>=2){{let a=parts.get(0)}};
- Float: let x=mut.0.0; x=s.tofloat(io.readln()); io.println(s.fromfloat(x));
- Comparison: = (eq) != (neq) < > <= >=
- Arrays use @() NOT [...]: let nums=@(1;2;3); — square brackets `[1,2,3]` are REJECTED by the parser.

CRITICAL REQUIREMENTS — your output WILL be rejected if any of these are missing:
1. Start with `m=<modulename>;` then your imports (i=io:std.io; etc) then function definitions
2. Define `f=main():$i64{{...<0}}` as the program entry point
3. Read input from stdin via `io.readln()` — do NOT hardcode test inputs
4. **Print the expected output to stdout via `io.println(...)`** — a program that compiles and runs but prints NOTHING fails validation
5. Return a complete program — not a snippet, fragment, or just the changed lines
6. NEVER use underscores in identifiers — `compute_cost` is REJECTED (E1003); the toke alphabet is a-z 0-9 plus 19 symbols only. Use camelCase (`computeCost`) or run-on (`computecost`).
7. Use toke keywords, NOT mainstream language ones: `mt` (not `match`), `lp` (not `for`/`while`), `el` (not `else`), `f=` (not `fn`/`def`), `<value` (not `return value`).

Return ONLY the complete fixed source code in ```toke ... ``` markers."""


def load_state() -> dict:
    """Load worker state from disk, or initialise fresh."""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            state = json.load(f)
        # Ensure category_stats exists (upgrade path for existing state files)
        if "category_stats" not in state:
            state["category_stats"] = {}
        return state
    return {
        "worker_id": WORKER_ID,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "completed": [],
        "failed": [],
        "skipped": [],
        "in_progress": None,
        "last_updated": None,
        "category_stats": {},
    }


# ---------------------------------------------------------------------------
# 107.R2 + R4 helpers
# ---------------------------------------------------------------------------
def load_budget() -> dict:
    """Load running Anthropic spend tally."""
    if BUDGET_FILE.exists():
        try:
            return json.loads(BUDGET_FILE.read_text())
        except Exception:
            pass
    return {"usd_spent": 0.0, "by_model": {}, "calls": 0, "passes": 0, "fails": 0}


def save_budget(b: dict):
    BUDGET_FILE.write_text(json.dumps(b, indent=2))


def record_call_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    b = load_budget()
    key = "opus" if "opus" in model.lower() else "sonnet"
    price = PRICE_PER_MTOK[key]
    cost = input_tokens * price["input"] / 1_000_000 + output_tokens * price["output"] / 1_000_000
    b["calls"] = b.get("calls", 0) + 1
    b["usd_spent"] = b.get("usd_spent", 0.0) + cost
    by = b["by_model"].setdefault(key, {"calls": 0, "input_tokens": 0, "output_tokens": 0, "usd": 0.0})
    by["calls"] += 1
    by["input_tokens"] += input_tokens
    by["output_tokens"] += output_tokens
    by["usd"] = by.get("usd", 0.0) + cost
    save_budget(b)
    return b["usd_spent"]


def budget_exceeded() -> bool:
    return load_budget()["usd_spent"] >= BUDGET_USD_CAP


def _dry_run_stub_source() -> str:
    """107.R4.1: deterministic valid-toke no-op used by DRY_RUN.
    Exercises compile + build + test paths without API spend."""
    return 'm=dryrun;i=io:std.io;f=main():$i64{io.println("dry-run-output");<0}'


def _looks_like_complete_program(src: str) -> bool:
    """107.R2: response-shape validation. Snippets fail this and trigger retry."""
    s = src.lstrip()
    return s.startswith("m=") and "f=main" in s


def _truncate_diagnostics(text: str, keep: int = 5) -> str:
    """107.R2: keep only first `keep` JSON diagnostic objects from tkc output.
    Cascading parser errors otherwise drown the prompt."""
    lines = text.splitlines()
    kept_diag = 0
    out_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("{") and '"error_code"' in stripped:
            kept_diag += 1
            if kept_diag > keep:
                if kept_diag == keep + 1:
                    out_lines.append(f"... ({len(lines) - len(out_lines)} more diagnostic lines truncated; fix the first {keep} first)")
                continue
        out_lines.append(line)
    return "\n".join(out_lines)


def _format_all_test_cases(test_cases: list) -> str:
    """107.R2: render ALL test cases as a numbered block for the repair prompt."""
    if not test_cases:
        return "  (no test cases defined)"
    lines = []
    for i, tc in enumerate(test_cases, 1):
        stdin = (tc.get("input", "") or "")[:400]
        expected = (tc.get("expected_output", "") or "")[:400]
        lines.append(f"  Test {i}:")
        lines.append(f"    stdin     = {stdin!r}")
        lines.append(f"    expected  = {expected!r}")
    return "\n".join(lines)


def _error_fingerprint(error: str) -> str:
    """107.R4.4: normalise an error string to a fingerprint for identical-fail detection."""
    if not error:
        return ""
    import re as _re
    # Primary error code
    m = _re.search(r'\bE\d{4}\b', error)
    code = m.group(0) if m else "noerr"
    # First message line, lower-cased, paths stripped, first 80 chars
    msg = error[:400]
    msg = _re.sub(r'/[\w/.-]+', '<path>', msg)
    msg = _re.sub(r'\s+', ' ', msg).strip().lower()[:80]
    return f"{code}|{msg}"


def get_repair_hint(req_id: str) -> str:
    """Pull program-specific hint from results/repair-hints.json if present."""
    hints_path = TEST_PROGRAMS_DIR / "results" / "repair-hints.json"
    if not hints_path.exists():
        return ""
    try:
        d = json.loads(hints_path.read_text())
        h = d.get(req_id, {})
        hints = h.get("hints", [])
        if hints:
            return "\nHINTS:\n" + "\n".join(f"  - {x}" for x in hints) + "\n"
    except Exception:
        pass
    return ""


def save_state(state: dict):
    """Persist state to disk atomically."""
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    tmp = STATE_FILE.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    tmp.rename(STATE_FILE)


# Categories ordered from simplest to most complex — AI agents last
CATEGORY_ORDER = [
    "calculators-finance", "education", "scientific-math", "devtools",
    "media-content", "data-processing", "system-tools", "games",
    "security", "messaging", "crypto-blockchain", "manufacturing-ml",
    "networking-rest", "social-media", "ai-agents",
]


def load_all_requirements() -> list[dict]:
    """Load all requirements from categories/*/requirements.yaml, ordered simple→complex."""
    requirements = []
    categories_dir = TEST_PROGRAMS_DIR / "categories"

    # Sort by CATEGORY_ORDER, unknown categories go to end
    def cat_sort_key(d):
        name = d.name
        if name in CATEGORY_ORDER:
            return CATEGORY_ORDER.index(name)
        return len(CATEGORY_ORDER)

    for category_dir in sorted(categories_dir.iterdir(), key=cat_sort_key):
        if not category_dir.is_dir():
            continue
        req_file = category_dir / "requirements.yaml"
        if not req_file.exists():
            continue

        with open(req_file) as f:
            content = yaml.safe_load(f)

        # requirements.yaml is a list of requirement dicts
        if isinstance(content, list):
            for req in content:
                req["_category"] = category_dir.name
                requirements.append(req)
        elif isinstance(content, dict) and "requirements" in content:
            for req in content["requirements"]:
                req["_category"] = category_dir.name
                requirements.append(req)

    return requirements


def is_my_work(req_id: str) -> bool:
    """Determine if this requirement belongs to this worker via hash partitioning."""
    h = int(hashlib.sha256(req_id.encode()).hexdigest(), 16)
    return (h % TOTAL_WORKERS) == (WORKER_ID - 1)


def solution_exists(category: str, req_id: str) -> bool:
    """Check if a verified solution already exists (in repo OR worker output)."""
    # Check repo (committed solutions)
    repo_dir = TEST_PROGRAMS_DIR / "categories" / category / req_id
    if (repo_dir / "solution.tk").exists():
        return True
    # Check worker solutions dir (previous run output)
    worker_dir = SOLUTIONS_DIR / category / req_id
    if (worker_dir / "solution.tk").exists():
        # Verify it still compiles with current tkc
        result = subprocess.run(
            ["tkc", "--check", str(worker_dir / "solution.tk")],
            capture_output=True, text=True, timeout=10,
        )
        if '"severity":"error"' not in (result.stdout + result.stderr):
            return True
    return False


def get_last_attempt(category: str, req_id: str) -> str | None:
    """Get the last failed attempt source to use as starting point for retry."""
    # Check failed dir for previous attempt
    fail_dir = FAILED_DIR / category / req_id
    last_attempt = fail_dir / "last-attempt.tk"
    if last_attempt.exists():
        return last_attempt.read_text()
    # Check solutions dir for a partially-working version
    sol_dir = SOLUTIONS_DIR / category / req_id
    sol_file = sol_dir / "solution.tk"
    if sol_file.exists():
        return sol_file.read_text()
    return None


CATEGORY_HALT_CHECK_INTERVAL = 20  # Check success rate every N programs
CATEGORY_HALT_THRESHOLD = 0.10  # Halt if success rate below 10%


def classify_error(error: str) -> str:
    """Classify an error string into a category for stats tracking."""
    error_lower = error.lower()
    # Compile errors: tkc --check failures with known error codes
    compile_codes = ["e4070", "e2002", "e2003", "e1003", "e3001", "e3002"]
    if any(code in error_lower for code in compile_codes):
        return "compile_error"
    if "compile error" in error_lower or "parse error" in error_lower:
        return "compile_error"
    # Build errors: link failures, codegen issues
    if "build failed" in error_lower or "build timeout" in error_lower:
        return "build_error"
    if "undefined reference" in error_lower or "link" in error_lower:
        return "build_error"
    if "binary not produced" in error_lower or "codegen" in error_lower:
        return "build_error"
    # Runtime errors: crashes, wrong output, timeouts during test
    if "timeout" in error_lower and "test" in error_lower:
        return "runtime_error"
    if "segfault" in error_lower or "crash" in error_lower or "signal" in error_lower:
        return "runtime_error"
    if "test failures" in error_lower or "expected" in error_lower:
        return "runtime_error"
    # Default to compile_error for unrecognised tkc output
    return "compile_error"


def update_category_stats(state: dict, category: str, passed: bool, error: str = ""):
    """Update category_stats in state with the result of processing a program."""
    if category not in state["category_stats"]:
        state["category_stats"][category] = {
            "attempted": 0, "passed": 0, "failed": 0, "skipped": 0,
        }
    stats = state["category_stats"][category]
    stats["attempted"] += 1
    if passed:
        stats["passed"] += 1
    else:
        stats["failed"] += 1
        # Track error type breakdown
        if error:
            err_type = classify_error(error)
            err_key = f"errors_{err_type}"
            stats[err_key] = stats.get(err_key, 0) + 1


def should_halt_category(state: dict, category: str) -> bool:
    """Check if a category should be halted due to low success rate.

    Returns True if we've attempted >= CATEGORY_HALT_CHECK_INTERVAL programs
    and the success rate is below CATEGORY_HALT_THRESHOLD.
    """
    stats = state.get("category_stats", {}).get(category)
    if not stats:
        return False
    attempted = stats["attempted"]
    if attempted < CATEGORY_HALT_CHECK_INTERVAL:
        return False
    # Only check at interval boundaries
    if attempted % CATEGORY_HALT_CHECK_INTERVAL != 0:
        return False
    success_rate = stats["passed"] / attempted if attempted > 0 else 0
    if success_rate < CATEGORY_HALT_THRESHOLD:
        log.warning(
            f"Category '{category}' halted: success rate {success_rate:.1%} "
            f"({stats['passed']}/{attempted}) is below {CATEGORY_HALT_THRESHOLD:.0%} threshold. "
            f"Stats: {json.dumps(stats)}"
        )
        return True
    return False


def try_compile_last_attempt(source: str, work_dir: Path) -> tuple[bool, str]:
    """Try compiling a last-attempt source with current tkc. Returns (compiles, output)."""
    source_path = work_dir / "solution.tk"
    source_path.write_text(source)
    return run_tkc_check(source_path)


def call_toke_api(description: str, req: dict) -> str | None:
    """Call api.tokelang.dev/v1/generate for initial code generation.
    107.R4.1: DRY_RUN=1 returns stub source without network call."""
    if DRY_RUN:
        log.info(f"  DRY_RUN: skipping toke API call, returning stub source")
        return _dry_run_stub_source()
    try:
        resp = requests.post(
            f"{TOKE_API_URL}/v1/generate",
            headers={
                "X-Api-Key": TOKE_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "description": description,
                "difficulty": req.get("difficulty", 2),
                "stdlib_modules": req.get("stdlib_modules", []),
                "input_format": req.get("input_format", ""),
                "output_format": req.get("output_format", ""),
            },
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("code") or data.get("source")
    except Exception as e:
        log.error(f"toke API call failed: {e}")
        return None


def call_anthropic_repair(source: str, error: str, description: str,
                          test_cases: list | None = None,
                          test_input: str = "", expected_output: str = "",
                          use_opus: bool = False,
                          req_id: str = "") -> str | None:
    """Call Anthropic API (Claude) to repair broken toke code.

    107.R2: test_cases list preferred over single test_input/expected fields.
    107.R4.1: DRY_RUN=1 returns _dry_run_stub_source() after prompt-format
    runs (catches IndexError/format crashes without API spend)."""
    model = "claude-opus-4-20250514" if use_opus else "claude-sonnet-4-20250514"
    # 107.R2: prefer full test_cases list
    if test_cases:
        all_tests = _format_all_test_cases(test_cases)
    elif test_input or expected_output:
        all_tests = _format_all_test_cases([{"input": test_input, "expected_output": expected_output}])
    else:
        all_tests = "  (no test cases provided)"
    user_content = TOKE_REPAIR_PROMPT.format(
        description=description,
        source=source,
        error=error,
        all_test_cases_block=all_tests,
        program_hints=get_repair_hint(req_id) if req_id else "",
    )
    # 107.R4.1: DRY_RUN short-circuit AFTER prompt-format so format crashes surface
    if DRY_RUN:
        log.info(f"  DRY_RUN: skipping Anthropic call ({req_id or 'noid'}), returning stub source")
        return _dry_run_stub_source()
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "max_tokens": 4096,
                "system": TOKE_SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": user_content}],
            },
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data["content"][0]["text"]

        # 107.R2: persist call cost from Anthropic usage block
        usage = data.get("usage", {}) or {}
        in_tok = int(usage.get("input_tokens", 0))
        out_tok = int(usage.get("output_tokens", 0))
        spent = record_call_cost(model, in_tok, out_tok)
        log.info(f"  spend ${spent:.4f}/{BUDGET_USD_CAP:.2f} ({model.split('-')[1]} in={in_tok} out={out_tok})")

        # Extract code from markdown fence if present
        if "```toke" in text:
            text = text.split("```toke", 1)[1].split("```", 1)[0]
        elif "```" in text:
            text = text.split("```", 1)[1].split("```", 1)[0]

        return text.strip()
    except Exception as e:
        log.error(f"Anthropic repair call failed: {e}")
        return None


def run_tkc_check(source_path: Path) -> tuple[bool, str]:
    """Run tkc --check on a source file. Returns (success, output)."""
    try:
        result = subprocess.run(
            ["tkc", "--check", str(source_path)],
            capture_output=True,
            text=True,
            timeout=TKC_TIMEOUT,
        )
        output = result.stdout + result.stderr
        return result.returncode == 0, output.strip()
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT: tkc --check exceeded time limit"
    except FileNotFoundError:
        return False, "ERROR: tkc not found in PATH"


def run_tests(solution_dir: Path, req: dict) -> tuple[bool, str]:
    """Run test cases against a compiled solution."""
    test_cases = req.get("test_cases", [])
    if not test_cases:
        return True, "No test cases defined"

    # Build the program using tkc --out (v0.3.2+ conditional linking)
    source_path = solution_dir / "solution.tk"
    try:
        time.sleep(BUILD_COOLDOWN)  # prevent OOM on small instances
        build_result = subprocess.run(
            ["tkc", "--out", str(solution_dir / "solution"), str(source_path)],
            capture_output=True,
            text=True,
            timeout=TKC_TIMEOUT,
        )
        if build_result.returncode != 0:
            return False, f"Build failed: {build_result.stderr[:500]}"
    except subprocess.TimeoutExpired:
        return False, "Build timeout"

    binary = solution_dir / "solution"
    if not binary.exists():
        return False, "Binary not produced"

    failures = []
    for i, tc in enumerate(test_cases):
        try:
            result = subprocess.run(
                [str(binary)],
                input=tc.get("input", ""),
                capture_output=True,
                text=True,
                timeout=TEST_TIMEOUT,
                errors="replace",  # 107.R3: cipher-style binary output shouldn't crash
            )
            actual = result.stdout.strip()
            expected = tc["expected_output"].strip()
            if actual != expected:
                failures.append(
                    f"Test {i+1}: expected '{expected}', got '{actual}'"
                )
        except subprocess.TimeoutExpired:
            failures.append(f"Test {i+1}: TIMEOUT")
        except Exception as e:
            failures.append(f"Test {i+1}: {e}")

    if failures:
        return False, "\n".join(failures)
    return True, f"All {len(test_cases)} tests passed"


def submit_feedback(req_id: str, success: bool, iterations: int):
    """Submit generation feedback to api.tokelang.dev."""
    try:
        requests.post(
            f"{TOKE_API_URL}/v1/feedback",
            headers={
                "X-Api-Key": TOKE_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "requirement_id": req_id,
                "success": success,
                "repair_iterations": iterations,
                "worker_id": WORKER_ID,
            },
            timeout=10,
        )
    except Exception as e:
        log.warning(f"Feedback submission failed for {req_id}: {e}")


def process_requirement(req: dict, state: dict):
    """Process a single requirement: generate, test, repair if needed."""
    req_id = req["id"]
    category = req["_category"]
    description = req.get("description", req.get("title", ""))

    log.info(f"Processing {req_id}: {req.get('title', '')}")
    state["in_progress"] = req_id
    save_state(state)

    # Working directory for this solution
    work_dir = SOLUTIONS_DIR / category / req_id
    work_dir.mkdir(parents=True, exist_ok=True)
    source_path = work_dir / "solution.tk"

    # Step 1: Check for previous attempt — try compiling before regenerating (102.34)
    previous = get_last_attempt(category, req_id)
    skip_generation = False
    if previous:
        log.info(f"{req_id}: Found previous attempt ({len(previous)} chars), checking if it compiles on current tkc")
        prev_compiles, prev_compile_output = try_compile_last_attempt(previous, work_dir)
        if prev_compiles:
            log.info(f"{req_id}: Previous attempt compiles on current tkc — skipping generation, going to build+test")
            source = previous
            skip_generation = True
        else:
            # Previous attempt doesn't compile — feed specific error to repair (not regenerate)
            log.info(f"{req_id}: Previous attempt has compile errors — will use as repair starting point")
            source = previous
    else:
        source = None

    if not skip_generation and source is None:
        # Fresh generation via toke API
        time.sleep(RATE_LIMIT_DELAY)
        source = call_toke_api(description, req)

    if not source:
        # Fallback: use Claude for initial generation if toke API is down
        log.info(f"{req_id}: Toke API unavailable, using Claude for initial generation")
        test_cases = req.get("test_cases", [])
        tc_input = test_cases[0].get("input", "") if test_cases else ""
        tc_output = test_cases[0].get("expected_output", "") if test_cases else ""
        gen_prompt = "Write a complete toke program: " + description
        if tc_input:
            gen_prompt += ". Input: " + tc_input.strip() + " Expected output: " + tc_output.strip()
        source = call_anthropic_repair(
            "m=placeholder;", "Need complete implementation", gen_prompt,
            test_input=tc_input, expected_output=tc_output, use_opus=False,
        )
        if not source:
            log.error(f"{req_id}: Claude fallback also failed")
            state["failed"].append({"id": req_id, "reason": "generation_failed"})
            update_category_stats(state, category, passed=False, error="generation_failed")
            state["in_progress"] = None
            save_state(state)
            return

    toke_api_source = source  # preserve original for metadata
    source_path.write_text(source)

    # Step 2: Compile check (also capture warnings)
    compiles, compile_output = run_tkc_check(source_path)
    warnings = [line for line in compile_output.split("\n") if "warning" in line.lower()]

    if compiles:
        # Step 3: Run tests
        passes, test_output = run_tests(work_dir, req)
        if passes:
            log.info(f"{req_id}: PASSED on first attempt (ONE-SHOT)")
            _save_success(req, work_dir, state, iterations=0,
                         toke_api_source=toke_api_source, warnings=warnings)
            update_category_stats(state, category, passed=True)
            submit_feedback(req_id, True, 0)
            return
        else:
            error = f"Test failures:\n{test_output}"
    else:
        error = f"Compile error:\n{compile_output}"

    # Step 4: Repair loop — capture every iteration as error→fix pair
    # Get test case info for the repair prompt
    test_cases = req.get("test_cases", [])
    test_input = test_cases[0].get("input", "") if test_cases else ""
    expected_output = test_cases[0].get("expected_output", "") if test_cases else ""

    repair_history = []
    for iteration in range(1, MAX_REPAIR_ITERATIONS + 1):
        use_opus = iteration > MAX_SONNET_ITERATIONS
        model_label = "opus" if use_opus else "sonnet"
        log.info(f"{req_id}: Repair iteration {iteration}/{MAX_REPAIR_ITERATIONS} ({model_label})")
        time.sleep(RATE_LIMIT_DELAY)

        broken_source = source  # save the broken version
        fixed_source = call_anthropic_repair(
            source, error, description,
            test_input=test_input, expected_output=expected_output,
            use_opus=use_opus,
        )
        if not fixed_source:
            log.warning(f"{req_id}: Repair returned nothing at iteration {iteration}")
            continue

        # Capture error→fix pair for training
        repair_history.append({
            "iteration": iteration,
            "broken_source": broken_source[:2000],
            "error": error[:1000],
            "fixed_source": fixed_source[:2000],
        })

        source = fixed_source
        source_path.write_text(source)

        compiles, compile_output = run_tkc_check(source_path)
        warnings = [line for line in compile_output.split("\n") if "warning" in line.lower()]

        if not compiles:
            error = f"Compile error:\n{compile_output}"
            continue

        passes, test_output = run_tests(work_dir, req)
        if passes:
            log.info(f"{req_id}: PASSED after {iteration} repair(s)")
            _save_success(req, work_dir, state, iterations=iteration,
                         toke_api_source=toke_api_source,
                         repair_history=repair_history, warnings=warnings)
            update_category_stats(state, category, passed=True)
            submit_feedback(req_id, True, iteration)
            return
        else:
            error = f"Test failures:\n{test_output}"

    # Failed after all repair attempts
    log.warning(f"{req_id}: FAILED after {MAX_REPAIR_ITERATIONS} repairs")
    _save_failure(req, work_dir, error, state)
    update_category_stats(state, category, passed=False, error=error)
    submit_feedback(req_id, False, MAX_REPAIR_ITERATIONS)


def _save_success(req: dict, work_dir: Path, state: dict, iterations: int,
                   toke_api_source: str = "", repair_history: list = None,
                   warnings: list = None):
    """Record a successful generation with full training metadata."""
    req_id = req["id"]

    # Generate companion file
    try:
        subprocess.run(
            [
                sys.executable,
                str(Path(__file__).parent / "worker-companion.py"),
                str(work_dir / "solution.tk"),
            ],
            timeout=120,
        )
    except Exception as e:
        log.warning(f"{req_id}: Companion generation failed: {e}")

    # Save string-stripped version for Stream 1 training
    source = (work_dir / "solution.tk").read_text()
    stripped = _strip_strings(source)
    (work_dir / "solution.stripped.tk").write_text(stripped)

    # Save toke API original (pre-repair) for comparison
    if toke_api_source:
        (work_dir / "toke_api_original.tk").write_text(toke_api_source)

    # Save error→fix pairs from repair history (training data for self-improvement)
    if repair_history:
        pairs_dir = work_dir / "repair_pairs"
        pairs_dir.mkdir(exist_ok=True)
        for i, pair in enumerate(repair_history):
            pair_file = pairs_dir / f"iteration_{i+1}.json"
            pair_file.write_text(json.dumps(pair, indent=2))

    # Write enriched metadata
    meta = {
        "id": req_id,
        "category": req["_category"],
        "title": req.get("title", ""),
        "description": req.get("description", "")[:500],
        "difficulty": req.get("difficulty", 0),
        "stdlib_modules": req.get("stdlib_modules", []),
        "repair_count": iterations,
        "one_shot": iterations == 0,
        "toke_api_compiled": bool(toke_api_source and iterations == 0),
        "warnings": warnings or [],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "worker_id": WORKER_ID,
        "source_chars": len(source),
        "source_lines": source.count("\n") + 1,
        "has_companion": (work_dir / "solution.tkc.md").exists(),
        "has_repair_pairs": bool(repair_history),
        "test_cases_count": len(req.get("test_cases", [])),
    }
    (work_dir / "meta.json").write_text(json.dumps(meta, indent=2))

    state["completed"].append(req_id)
    state["in_progress"] = None
    save_state(state)


def _strip_strings(source: str) -> str:
    """Replace string contents with '_' for Stream 1 training data."""
    import re
    return re.sub(r'"[^"]*"', '"_"', source)


def _save_failure(req: dict, work_dir: Path, last_error: str, state: dict):
    """Record a failed generation."""
    req_id = req["id"]
    category = req["_category"]

    fail_dir = FAILED_DIR / category / req_id
    fail_dir.mkdir(parents=True, exist_ok=True)

    # Copy last attempt source
    source_path = work_dir / "solution.tk"
    if source_path.exists():
        (fail_dir / "last-attempt.tk").write_text(source_path.read_text())

    # Save error log
    (fail_dir / "error.log").write_text(last_error)

    state["failed"].append({"id": req_id, "reason": "max_repairs_exceeded"})
    state["in_progress"] = None
    save_state(state)


def main():
    """Main loop: load requirements, filter to this worker's partition, process."""
    log.info(f"Worker {WORKER_ID}/{TOTAL_WORKERS} starting")

    if TOKE_API_KEY == "PLACEHOLDER" or ANTHROPIC_API_KEY == "PLACEHOLDER":
        log.error("API keys not configured. Edit /opt/toke-worker/.env")
        sys.exit(1)

    # Pull latest test programs
    try:
        subprocess.run(
            ["git", "fetch", "origin", "main"],
            cwd=TEST_PROGRAMS_DIR,
            capture_output=True, timeout=30,
        )
        subprocess.run(
            ["git", "reset", "--hard", "origin/main"],
            cwd=TEST_PROGRAMS_DIR,
            capture_output=True, timeout=10,
        )
    except Exception:
        pass

    state = load_state()
    all_requirements = load_all_requirements()
    log.info(f"Loaded {len(all_requirements)} total requirements")

    # Filter to this worker's partition, then sort by category order (simple first)
    my_requirements = [r for r in all_requirements if is_my_work(r["id"])]
    cat_order = {c: idx for idx, c in enumerate(CATEGORY_ORDER)}
    my_requirements.sort(key=lambda r: cat_order.get(r["_category"], len(CATEGORY_ORDER)))
    log.info(f"This worker handles {len(my_requirements)} requirements")
    log.info(f"Category order: {', '.join(dict.fromkeys(r['_category'] for r in my_requirements))}")

    # Only skip completed programs — retry failed ones (they may work with new compiler/prompts)
    completed_ids = set(state["completed"] + state["skipped"])
    failed_ids = set(f["id"] if isinstance(f, dict) else f for f in state["failed"])

    # Track which categories have been halted due to low success rate (102.32)
    halted_categories = set()

    for req in my_requirements:
        req_id = req["id"]
        category = req["_category"]

        # Skip entire category if halted due to low success rate (102.32)
        if category in halted_categories:
            if req_id not in completed_ids:
                state["skipped"].append(req_id)
                # Update category stats with skip count
                if category in state["category_stats"]:
                    state["category_stats"][category]["skipped"] = \
                        state["category_stats"][category].get("skipped", 0) + 1
                save_state(state)
            continue

        # Skip completed (already working)
        if req_id in completed_ids:
            continue

        # Skip if verified solution already exists on disk
        if solution_exists(req["_category"], req_id):
            log.info(f"{req_id}: Verified solution exists, skipping")
            if req_id not in completed_ids:
                state["completed"].append(req_id)
                save_state(state)
            continue

        # Remove from failed list if retrying (clean slate for this attempt)
        if req_id in failed_ids:
            log.info(f"{req_id}: Retrying previously failed program")
            state["failed"] = [f for f in state["failed"] if (f.get("id") if isinstance(f, dict) else f) != req_id]
            save_state(state)
            log.info(f"{req_id}: Solution already exists, skipping")
            state["skipped"].append(req_id)
            save_state(state)
            continue

        process_requirement(req, state)

        # After processing, check if this category should be halted (102.32)
        if should_halt_category(state, category):
            halted_categories.add(category)
            cat_stats = state["category_stats"].get(category, {})
            log.info(
                f"Moving to next category. '{category}' final stats: "
                f"attempted={cat_stats.get('attempted', 0)}, "
                f"passed={cat_stats.get('passed', 0)}, "
                f"failed={cat_stats.get('failed', 0)}, "
                f"skipped={cat_stats.get('skipped', 0)}"
            )

        # Periodic S3 sync every 50 programs
        total_done = len(state["completed"]) + len(state["failed"])
        if total_done > 0 and total_done % 50 == 0:
            log.info(f"Periodic S3 sync at {total_done} programs...")
            sync_to_s3()

    log.info(
        f"Worker {WORKER_ID} complete. "
        f"Passed: {len(state['completed'])}, "
        f"Failed: {len(state['failed'])}, "
        f"Skipped: {len(state['skipped'])}"
    )

    # Sync results to S3
    sync_to_s3()

    # Auto-stop this instance
    log.info("All work complete. Stopping instance.")
    subprocess.run(["sudo", "shutdown", "-h", "now"], check=False)


def sync_to_s3():
    """Sync completed solutions to S3 bucket. Non-fatal if aws cli unavailable."""
    try:
        s3_bucket = os.environ.get("S3_BUCKET", "toke-test-programs")
        s3_region = os.environ.get("S3_REGION", "ap-southeast-2")
        solutions_dir = WORKER_DIR / "solutions"
        if solutions_dir.exists():
            log.info(f"Syncing solutions to s3://{s3_bucket}/worker-{WORKER_ID}/")
            subprocess.run([
                "aws", "s3", "sync",
                str(solutions_dir),
                f"s3://{s3_bucket}/worker-{WORKER_ID}/",
                "--region", s3_region,
            ], check=False)
        state_file = WORKER_DIR / "state.json"
        if state_file.exists():
            subprocess.run([
                "aws", "s3", "cp",
                str(state_file),
                f"s3://{s3_bucket}/worker-{WORKER_ID}/state.json",
                "--region", s3_region,
            ], check=False)
    except Exception as e:
        log.warning(f"S3 sync skipped: {e}")


if __name__ == "__main__":
    main()

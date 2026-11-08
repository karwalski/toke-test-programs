#!/usr/bin/env python3
"""136.80 gate: no program runs a shell command line built from input.

A program that hands `/bin/sh -c` a string it assembled from input values
lets a quote, `;`, `$(...)` or backtick in that input run as a command (the
SYS-102 class, ADR-0011: argv-only exec).  This scans every
results/solutions/*/*/solution.tk for an argv array literal that starts with
a shell and `-c`, and looks at the script argument:

  * a string literal (no `\\(...)` interpolation)       -> fine
  * a parameter of the enclosing function, and every call
    of that function passes a string literal there     -> fine
  * anything else                                      -> FLAGGED

A program whose job is to run its input as a shell command (a command
runner) is listed in ALLOW with the reason.  An ALLOW entry that is no longer
flagged is reported as stale, so the list cannot outlive its programs.

    python3 scripts/check-shell-spawn.py        # exit 1 on any finding
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# id -> why its shell script argument may come from input.
ALLOW = {
    "SYS-051": "command differ: lines 1-2 are shell commands to run and diff, by design",
    "SYS-077": "script runner with timeout: line 2 is the shell command, by design; "
               "the timeout is passed as $1, never spliced into the script (136.80)",
    "SYS-088": "background task runner: each input line is a shell command, by design",
    "SYS-112": "menu runner: each menu item is LABEL: COMMAND, a shell command by design",
    "SYS-121": "watch: line 3 is the shell command to repeat, by design",
}

SHELLS = ("sh", "/bin/sh", "bash", "/bin/bash", "zsh", "/bin/zsh", "dash", "/bin/dash")
SHELL_ARGV = re.compile(r'@\(\s*"(%s)"\s*;\s*"-c"\s*;' % "|".join(re.escape(s) for s in SHELLS))
LITERAL = re.compile(r'"(?:[^"\\]|\\.)*"\Z', re.S)
FUNC = re.compile(r'(?<![\w.])f=(\w+)\(([^)]*)\)')


def arg_at(src, i):
    """The argument starting at src[i], up to the `;` or `)` that ends it at
    nesting depth 0 (string-aware): (its text, the terminator's index)."""
    depth, j, n = 0, i, len(src)
    while j < n:
        c = src[j]
        if c == '"':
            j += 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            if depth == 0:
                break
            depth -= 1
        elif c == ";" and depth == 0:
            break
        j += 1
    return src[i:j].strip(), j


def is_literal(text):
    return bool(LITERAL.match(text)) and "\\(" not in text


def literal_param(src, pos, name):
    """True when `name` is a parameter of the function enclosing `pos` and
    every call of that function passes a string literal in its place."""
    defs = [m for m in FUNC.finditer(src) if m.start() < pos]
    if not defs:
        return False
    fn, params = defs[-1].group(1), defs[-1].group(2)
    names = [p.split(":")[0].strip() for p in params.split(";") if p.strip()]
    if name not in names:
        return False
    k = names.index(name)
    for call in re.finditer(r'(?<![\w.])%s\(' % re.escape(fn), src):
        if src[max(0, call.start() - 2):call.start()] == "f=":
            continue  # the definition, not a call
        j = call.end()
        for _ in range(k + 1):
            arg, end = arg_at(src, j)
            j = end + 1
        if not is_literal(arg):
            return False
    return True


def findings(src):
    out = []
    for m in SHELL_ARGV.finditer(src):
        script, _ = arg_at(src, m.end())
        if is_literal(script):
            continue
        if re.fullmatch(r"\w+", script) and literal_param(src, m.start(), script):
            continue
        line = src.count("\n", 0, m.start()) + 1
        out.append(f"line {line}: {m.group(1)} -c {script[:60]}")
    return out


def main():
    sols = sorted(glob.glob(os.path.join(ROOT, "results", "solutions", "*", "*", "solution.tk")))
    if len(sols) < 1000:
        print(f"check-shell-spawn: only {len(sols)} solutions found -- wrong tree?")
        return 2
    bad, allowed = [], set()
    for sol in sols:
        pid = os.path.basename(os.path.dirname(sol))
        hits = findings(open(sol, encoding="utf-8", errors="replace").read())
        if not hits:
            continue
        if pid in ALLOW:
            allowed.add(pid)
            continue
        bad += [f"{os.path.relpath(sol, ROOT)}: {h}" for h in hits]
    stale = sorted(set(ALLOW) - allowed)
    for b in bad:
        print(f"SHELL-FROM-INPUT {b}")
    for s in stale:
        print(f"STALE allowlist entry {s}: no longer runs a shell on input -- remove it")
    print(f"check-shell-spawn: {len(sols)} programs, {len(allowed)} allowlisted runners, "
          f"{len(bad)} finding(s), {len(stale)} stale")
    return 1 if (bad or stale) else 0


if __name__ == "__main__":
    sys.exit(main())

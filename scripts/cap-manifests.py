#!/usr/bin/env python3
"""126.3 — capability grants (ADR-0010) for the library programs.

A toke binary is deny-by-default: a call into the file system, the network,
the environment or a subprocess aborts with CAP001 unless the build granted
that class.  Every harness in this repo compiled with `--allow-all`, so no
library program ever declared what it needs, and a program copied out of the
library and built the documented way failed at its first `file.read`.

This script derives each library program's grants from the calls in its
`solution.tk` and writes them to `tkc.toml` beside it.  The harnesses compile
with `--config=<that tkc.toml>` instead of `--allow-all`, so a grant that is
missing shows up as a failing test rather than being papered over.

The mapping is the stdlib's own gate (`TK_REQUIRE(...)` in toke's
`src/stdlib/*_glue.c`, `os.c`, `http.c`), keyed by module and function.  It is
deliberately a table, not a guess: a call whose module is gated but whose
function is not in the table is an error, so a new gated function cannot be
silently left ungranted.

    python3 scripts/cap-manifests.py --write   # (re)write the manifests
    python3 scripts/cap-manifests.py --check   # gate: exit 1 on any drift
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R, W, NET, ENV, RUN = "fs_read", "fs_write", "net", "env_write", "process_spawn"
ORDER = (R, W, NET, ENV, RUN)

# module -> {function: grants}.  A module listed here is GATED: every function
# called on it must appear (possibly with no grants).
GATED = {
    "file": {
        "read": {R}, "exists": {R}, "isdir": {R}, "list": {R}, "listall": {R},
        "stat": {R}, "readlines": {R}, "listglob": {R}, "readbytes": {R},
        "readrange": {R}, "size": {R},
        "write": {W}, "mkdir": {W}, "append": {W}, "delete": {W}, "rename": {W},
        "writelines": {W}, "appendline": {W}, "ensuredir": {W}, "writebytes": {W},
        "copy": {R, W},
    },
    # std.fs is a second, smaller file surface over the same gated glue
    # (found by the full-library run: SYS-115 hit CAP001 fs.write).
    "fs": {"read": {R}, "write": {W}, "writetext": {W}},
    "process": {"spawn": {RUN}, "exec": {RUN}, "spawndetached": {RUN},
                "stdout": set(), "stderr": set(), "wait": set(), "kill": set()},
    "env": {"set": {ENV}, "get": set(), "getor": set(), "getint": set(), "expand": set()},
    "os": {"open": {R, W}, "stat": {R}, "access": {R}, "unlink": {W}, "rename": {W},
           "mkdir": {W}, "rmdir": {W}, "setenv": {ENV}, "getpid": set()},
    "net": {"portavailable": {NET}, "listen": {NET}, "accept": {NET}},
    # http: the server (http_serve / bind_listen) and the client
    # (client_tcp_connect) need net; registering a route does not.
    "http": {"serve": {NET}, "servetls": {NET}, "serveworkers": {NET}, "listen": {NET},
             "servedir": set(), "servepages": set(),
             "postjson": {NET}, "postheaders": {NET}, "posturl": {NET}, "client": {NET},
             "get": set(), "post": set(), "put": set(), "delete": set(), "patch": set(),
             "head": set(), "getstatic": set(), "poststatic": set(), "status": set(),
             "body": set(), "res": set(), "resok": set(), "resbad": set(), "reserr": set(),
             "resjson": set(), "param": set(), "header": set(), "setcors": set(),
             "setnotfound": set()},
    "ws": {"connect": {NET}, "send": set(), "sendbytes": set(), "recv": set(),
           "close": set(), "broadcast": set()},
    "tls": {"connect": {NET}, "listen": {NET}},
}
IMPORT = re.compile(r"\bi=(\w+):std\.(\w+)\s*;")


def library():
    """(category, id) of every program in the published library."""
    out = []
    for cf in sorted(glob.glob(os.path.join(ROOT, "results", "library", "*.json"))):
        if cf.endswith("index.json"):
            continue
        d = json.load(open(cf))
        out += [(d["category"], p["id"]) for p in d["programs"]]
    return out


def grants(src):
    """(set of grants, [unknown gated calls]) for one program's source."""
    need, unknown = set(), []
    for alias, mod in IMPORT.findall(src):
        if mod not in GATED:
            continue
        for fn in re.findall(r"(?<![\w.])" + re.escape(alias) + r"\.(\w+)\s*\(", src):
            if fn in GATED[mod]:
                need |= GATED[mod][fn]
            else:
                unknown.append(f"{mod}.{fn}")
    return need, sorted(set(unknown))


def render(need):
    lines = ["# 126.3: capability grants (ADR-0010), derived from the calls in",
             "# solution.tk by scripts/cap-manifests.py -- regenerate, do not edit.",
             "[capabilities]"]
    lines += [f"{k} = true" for k in ORDER if k in need]
    return "\n".join(lines) + "\n"


def main():
    write = "--write" in sys.argv
    if not write and "--check" not in sys.argv:
        print(__doc__)
        return 2
    progs = library()
    if len(progs) < 1000:
        print(f"cap-manifests: only {len(progs)} library programs found -- wrong tree?")
        return 2
    drift, unknown, granted = [], [], 0
    for cat, pid in progs:
        d = os.path.join(ROOT, "results", "solutions", cat, pid)
        sol = os.path.join(d, "solution.tk")
        if not os.path.exists(sol):
            continue
        need, unk = grants(open(sol, encoding="utf-8", errors="replace").read())
        unknown += [f"{cat}/{pid}: {u}" for u in unk]
        man = os.path.join(d, "tkc.toml")
        want = render(need) if need else None
        have = open(man).read() if os.path.exists(man) else None
        granted += bool(need)
        if want == have:
            continue
        if write:
            if want is None:
                os.remove(man)
            else:
                open(man, "w").write(want)
        else:
            drift.append(f"{cat}/{pid}: tkc.toml "
                         + ("missing" if have is None else "stale" if want else "grants nothing -- remove it"))
    for u in unknown:
        print(f"UNKNOWN gated call (add it to GATED): {u}")
    for x in drift:
        print(f"DRIFT {x}")
    print(f"cap-manifests: {len(progs)} library programs, {granted} need grants, "
          f"{len(drift)} drift, {len(unknown)} unknown gated call(s)")
    return 1 if (drift or unknown) else 0


if __name__ == "__main__":
    sys.exit(main())

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

WORKER_DIR = Path("/opt/toke-worker")
REPOS_DIR = WORKER_DIR / "repos"
TEST_PROGRAMS_DIR = REPOS_DIR / "toke-test-programs"
STATE_FILE = WORKER_DIR / "state.json"
LOGS_DIR = WORKER_DIR / "logs"
SOLUTIONS_DIR = WORKER_DIR / "solutions"
FAILED_DIR = WORKER_DIR / "failed"

MAX_SONNET_ITERATIONS = 10
MAX_OPUS_ITERATIONS = 5
MAX_REPAIR_ITERATIONS = MAX_SONNET_ITERATIONS + MAX_OPUS_ITERATIONS  # 15 total
RATE_LIMIT_DELAY = 1.0  # seconds between API calls
TKC_TIMEOUT = 60  # seconds (increased for tkc --out full build)
TEST_TIMEOUT = 10  # seconds
BUILD_COOLDOWN = 2.0  # seconds between builds to prevent OOM on small instances

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
TOKE_SYSTEM_PROMPT = """You write toke programs. toke is a compiled language.

STRUCTURE: m=name; then i=alias:std.module; then f= and t= declarations.
KEYWORDS (13): m f t i if el lp br let mut as rt mt
CRITICAL RULES:
- Semicolons separate ALL statements and parameters. NO COMMAS anywhere.
- No square brackets. Arrays: @(1;2;3). Array access: arr.get(idx).
- Functions: f=name(param:$i64;param2:$str):$i64{body}
- Return: <expr; (preferred) or rt expr;
- Loops: lp(let idx=0;idx<n;idx=idx+1){body}
- Mutable: let x=mut.0; then x=x+1;
- Types use $ prefix: $i64, $f64, $str, $bool, $void. ALL types need $.
- Equality is = not ==. Comparison: < > !=
- Module: m=name; (first line, always)
- Import: i=alias:std.module; then use alias.func()
- NEVER use i/f/t/m as variable names — they are keywords.
- No 'return', 'fn', 'func', 'for', 'while', 'else', 'int', 'string' — these are NOT toke.
- io.println(value) prints to stdout. io.readln() reads line from stdin.
- str.toint(s) parses integer. str.fromint(n) converts int to string.

WORKING EXAMPLES:
m=fact;i=io:std.io;i=s:std.str;f=fact(n:$i64):$i64{if(n<2){<1};<n*fact(n-1)};f=main():$i64{let line=io.readln();let n=s.toint(line);io.println(s.fromint(fact(n)));<0}

m=fizz;i=io:std.io;i=s:std.str;f=main():$i64{let line=io.readln();let n=s.toint(line);if(n%15=0){io.println("fizzbuzz");<0};if(n%3=0){io.println("fizz");<0};if(n%5=0){io.println("buzz");<0};io.println(s.fromint(n));<0}

Output ONLY toke source code. No explanation. No markdown fences unless asked."""

TOKE_REPAIR_PROMPT = """Fix this toke program. The error is shown below.

REQUIREMENT: {description}
INPUT: {test_input}
EXPECTED OUTPUT: {expected_output}

CURRENT SOURCE:
```toke
{source}
```

ERROR:
{error}

RULES REMINDER:
- m= module first, i= imports, f= functions. Semicolons everywhere. NO COMMAS.
- Types: $i64, $str, $bool (always with $). Equality: = not ==.
- io.readln() reads stdin, io.println(x) writes stdout
- str.toint(s) parses int, str.fromint(n) int to string
- Arrays: @(). Loop: lp(let idx=0;idx<n;idx=idx+1){{}}
- NEVER use i/f/t/m as variable names. Use idx, k, n, x, val, acc.
- No 'return'/'fn'/'for'/'while'/'else' — use </rt/f=/lp/el

Return ONLY the fixed toke source code wrapped in ```toke ... ``` markers."""


def load_state() -> dict:
    """Load worker state from disk, or initialise fresh."""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "worker_id": WORKER_ID,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "completed": [],
        "failed": [],
        "skipped": [],
        "in_progress": None,
        "last_updated": None,
    }


def save_state(state: dict):
    """Persist state to disk atomically."""
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    tmp = STATE_FILE.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    tmp.rename(STATE_FILE)


def load_all_requirements() -> list[dict]:
    """Load all requirements from categories/*/requirements.yaml."""
    requirements = []
    categories_dir = TEST_PROGRAMS_DIR / "categories"

    for category_dir in sorted(categories_dir.iterdir()):
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
    """Check if a solution already exists in the repo."""
    solution_dir = TEST_PROGRAMS_DIR / "categories" / category / req_id
    return (solution_dir / "solution.tk").exists()


def call_toke_api(description: str, req: dict) -> str | None:
    """Call api.tokelang.dev/v1/generate for initial code generation."""
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
                          test_input: str = "", expected_output: str = "",
                          use_opus: bool = False) -> str | None:
    """Call Anthropic API (Claude) to repair broken toke code."""
    model = "claude-opus-4-20250514" if use_opus else "claude-sonnet-4-20250514"
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
                "messages": [
                    {
                        "role": "user",
                        "content": TOKE_REPAIR_PROMPT.format(
                            description=description,
                            source=source,
                            error=error,
                            test_input=test_input[:200],
                            expected_output=expected_output[:200],
                        ),
                    }
                ],
            },
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data["content"][0]["text"]

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

    # Step 1: Initial generation via toke API
    time.sleep(RATE_LIMIT_DELAY)
    source = call_toke_api(description, req)

    if not source:
        log.error(f"{req_id}: Initial generation returned nothing")
        state["failed"].append({"id": req_id, "reason": "generation_failed"})
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
            submit_feedback(req_id, True, iteration)
            return
        else:
            error = f"Test failures:\n{test_output}"

    # Failed after all repair attempts
    log.warning(f"{req_id}: FAILED after {MAX_REPAIR_ITERATIONS} repairs")
    _save_failure(req, work_dir, error, state)
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

    # Filter to this worker's partition
    my_requirements = [r for r in all_requirements if is_my_work(r["id"])]
    log.info(f"This worker handles {len(my_requirements)} requirements")

    done_ids = set(state["completed"] + [f["id"] if isinstance(f, dict) else f for f in state["failed"]] + state["skipped"])

    for req in my_requirements:
        req_id = req["id"]

        # Skip already processed
        if req_id in done_ids:
            continue

        # Skip if solution already exists in repo
        if solution_exists(req["_category"], req_id):
            log.info(f"{req_id}: Solution already exists, skipping")
            state["skipped"].append(req_id)
            save_state(state)
            continue

        process_requirement(req, state)

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

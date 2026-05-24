#!/usr/bin/env bash
# test-runner.sh — Run tests for a single toke program directory.
#
# Usage: ./scripts/test-runner.sh categories/games/GAM-001/
#
# Expects the directory to contain:
#   solution.tk
#   tests/input_*.txt
#   tests/expected_*.txt
#
# Reports per test: PASS/FAIL/TIMEOUT/COMPILE_ERROR
# Logs compiler bugs to issues/compiler-bugs.jsonl
# Logs test failures to issues/test-failures.jsonl
# Optionally submits feedback to api.tokelang.dev/v1/feedback

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ISSUES_DIR="$BASE_DIR/issues"
TIMEOUT_SECONDS=10

# Ensure issues directory exists
mkdir -p "$ISSUES_DIR"

# Validate arguments
if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <program-directory>"
    echo "  e.g. $0 categories/games/GAM-001/"
    exit 2
fi

PROGRAM_DIR="$1"

# Resolve relative paths against base dir
if [[ ! "$PROGRAM_DIR" = /* ]]; then
    PROGRAM_DIR="$BASE_DIR/$PROGRAM_DIR"
fi

if [[ ! -d "$PROGRAM_DIR" ]]; then
    echo "ERROR: Directory not found: $PROGRAM_DIR"
    exit 2
fi

SOLUTION="$PROGRAM_DIR/solution.tk"
TESTS_DIR="$PROGRAM_DIR/tests"

if [[ ! -f "$SOLUTION" ]]; then
    echo "ERROR: No solution.tk found in $PROGRAM_DIR"
    exit 2
fi

if [[ ! -d "$TESTS_DIR" ]]; then
    echo "ERROR: No tests/ directory found in $PROGRAM_DIR"
    exit 2
fi

# Extract program ID from directory name
PROGRAM_ID="$(basename "$PROGRAM_DIR")"
CATEGORY="$(basename "$(dirname "$PROGRAM_DIR")")"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# --- Step 1: Compile check ---
echo "=== Testing: $CATEGORY/$PROGRAM_ID ==="
echo ""

COMPILE_OUTPUT=""
COMPILE_EXIT=0
COMPILE_OUTPUT=$(tkc --check "$SOLUTION" 2>&1) || COMPILE_EXIT=$?

if [[ $COMPILE_EXIT -ne 0 ]]; then
    echo "COMPILE_ERROR: tkc --check failed"
    echo "$COMPILE_OUTPUT"
    echo ""

    # Log to compiler-bugs.jsonl
    # Escape JSON strings
    ESCAPED_OUTPUT=$(echo "$COMPILE_OUTPUT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
    cat >> "$ISSUES_DIR/compiler-bugs.jsonl" <<EOF
{"timestamp":"$TIMESTAMP","program_id":"$PROGRAM_ID","category":"$CATEGORY","solution":"$SOLUTION","diagnostic":$ESCAPED_OUTPUT}
EOF

    echo "RESULT: 0/0 tests passed (COMPILE_ERROR)"
    exit 1
fi

echo "Compile check: OK"

# --- Step 2: Build ---
BUILD_DIR=$(mktemp -d)
trap "rm -rf $BUILD_DIR" EXIT

BUILD_OUTPUT=""
BUILD_EXIT=0
BUILD_OUTPUT=$(tkc --emit-llvm --out "$BUILD_DIR/solution.ll" "$SOLUTION" 2>&1) || BUILD_EXIT=$?

if [[ $BUILD_EXIT -ne 0 ]]; then
    echo "COMPILE_ERROR: tkc --emit-llvm failed"
    echo "$BUILD_OUTPUT"

    ESCAPED_OUTPUT=$(echo "$BUILD_OUTPUT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
    cat >> "$ISSUES_DIR/compiler-bugs.jsonl" <<EOF
{"timestamp":"$TIMESTAMP","program_id":"$PROGRAM_ID","category":"$CATEGORY","solution":"$SOLUTION","stage":"emit-llvm","diagnostic":$ESCAPED_OUTPUT}
EOF

    echo "RESULT: 0/0 tests passed (COMPILE_ERROR at emit-llvm)"
    exit 1
fi

LINK_OUTPUT=""
LINK_EXIT=0
LINK_OUTPUT=$(clang "$BUILD_DIR/solution.ll" -o "$BUILD_DIR/solution" -lm 2>&1) || LINK_EXIT=$?

if [[ $LINK_EXIT -ne 0 ]]; then
    echo "COMPILE_ERROR: clang link failed"
    echo "$LINK_OUTPUT"

    ESCAPED_OUTPUT=$(echo "$LINK_OUTPUT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
    cat >> "$ISSUES_DIR/compiler-bugs.jsonl" <<EOF
{"timestamp":"$TIMESTAMP","program_id":"$PROGRAM_ID","category":"$CATEGORY","solution":"$SOLUTION","stage":"link","diagnostic":$ESCAPED_OUTPUT}
EOF

    echo "RESULT: 0/0 tests passed (COMPILE_ERROR at link)"
    exit 1
fi

echo "Build: OK"
echo ""

# --- Step 3: Run tests ---
TOTAL=0
PASSED=0
FAILED=0
TIMED_OUT=0

for INPUT_FILE in "$TESTS_DIR"/input_*.txt; do
    [[ -f "$INPUT_FILE" ]] || continue

    # Derive expected file name: input_01.txt -> expected_01.txt
    BASENAME=$(basename "$INPUT_FILE")
    TEST_NUM="${BASENAME#input_}"
    EXPECTED_FILE="$TESTS_DIR/expected_$TEST_NUM"

    if [[ ! -f "$EXPECTED_FILE" ]]; then
        echo "  SKIP: No expected file for $BASENAME"
        continue
    fi

    TOTAL=$((TOTAL + 1))
    ACTUAL_FILE="$BUILD_DIR/actual_$TEST_NUM"

    # Run with timeout
    RUN_EXIT=0
    timeout "$TIMEOUT_SECONDS" "$BUILD_DIR/solution" < "$INPUT_FILE" > "$ACTUAL_FILE" 2>/dev/null || RUN_EXIT=$?

    if [[ $RUN_EXIT -eq 124 ]]; then
        echo "  TIMEOUT: test $TEST_NUM (>${TIMEOUT_SECONDS}s)"
        TIMED_OUT=$((TIMED_OUT + 1))
        continue
    fi

    # Compare output
    if diff -q "$ACTUAL_FILE" "$EXPECTED_FILE" > /dev/null 2>&1; then
        echo "  PASS: test $TEST_NUM"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: test $TEST_NUM"
        FAILED=$((FAILED + 1))

        # Log failure
        INPUT_CONTENT=$(python3 -c "import sys,json; print(json.dumps(open(sys.argv[1]).read()))" "$INPUT_FILE")
        EXPECTED_CONTENT=$(python3 -c "import sys,json; print(json.dumps(open(sys.argv[1]).read()))" "$EXPECTED_FILE")
        ACTUAL_CONTENT=$(python3 -c "import sys,json; print(json.dumps(open(sys.argv[1]).read()))" "$ACTUAL_FILE")

        cat >> "$ISSUES_DIR/test-failures.jsonl" <<EOF
{"timestamp":"$TIMESTAMP","program_id":"$PROGRAM_ID","category":"$CATEGORY","test":"$TEST_NUM","input":$INPUT_CONTENT,"expected":$EXPECTED_CONTENT,"actual":$ACTUAL_CONTENT}
EOF
    fi
done

echo ""
echo "RESULT: $PASSED/$TOTAL tests passed (failed=$FAILED, timeout=$TIMED_OUT)"

# --- Step 4: Optional API feedback ---
if [[ -n "${TOKE_API_KEY:-}" ]]; then
    FEEDBACK_PAYLOAD=$(cat <<EOF
{
    "program_id": "$PROGRAM_ID",
    "category": "$CATEGORY",
    "timestamp": "$TIMESTAMP",
    "total_tests": $TOTAL,
    "passed": $PASSED,
    "failed": $FAILED,
    "timed_out": $TIMED_OUT
}
EOF
)
    curl -s -X POST "https://api.tokelang.dev/v1/feedback" \
        -H "Authorization: Bearer $TOKE_API_KEY" \
        -H "Content-Type: application/json" \
        -d "$FEEDBACK_PAYLOAD" > /dev/null 2>&1 || true
fi

# Exit with failure if any tests didn't pass
if [[ $PASSED -lt $TOTAL ]]; then
    exit 1
fi

exit 0

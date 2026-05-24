#!/usr/bin/env bash
# run-all.sh — Run test-runner.sh on all program directories with solution.tk.
#
# Produces summary report and outputs results to reports/run-<date>.json.
#
# Usage: ./scripts/run-all.sh

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPORTS_DIR="$BASE_DIR/reports"
TEST_RUNNER="$SCRIPT_DIR/test-runner.sh"

# Ensure directories exist
mkdir -p "$REPORTS_DIR"

TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DATE_SLUG="$(date +%Y%m%d-%H%M%S)"
REPORT_FILE="$REPORTS_DIR/run-${DATE_SLUG}.json"

# Counters
TOTAL_PROGRAMS=0
COMPILE_ERRORS=0
PASS_COUNT=0
FAIL_COUNT=0
TIMEOUT_COUNT=0

# Collect per-program results
RESULTS_JSON="[]"

echo "============================================================"
echo "TOKE TEST PROGRAMS - FULL TEST RUN"
echo "Started: $TIMESTAMP"
echo "============================================================"
echo ""

# Find all directories containing solution.tk
while IFS= read -r SOLUTION_FILE; do
    PROGRAM_DIR="$(dirname "$SOLUTION_FILE")"
    PROGRAM_ID="$(basename "$PROGRAM_DIR")"
    CATEGORY="$(basename "$(dirname "$PROGRAM_DIR")")"

    # Skip if no tests directory
    if [[ ! -d "$PROGRAM_DIR/tests" ]]; then
        continue
    fi

    TOTAL_PROGRAMS=$((TOTAL_PROGRAMS + 1))

    # Run test-runner and capture output
    OUTPUT=""
    EXIT_CODE=0
    OUTPUT=$("$TEST_RUNNER" "$PROGRAM_DIR" 2>&1) || EXIT_CODE=$?

    # Parse result from output
    RESULT_LINE=$(echo "$OUTPUT" | grep "^RESULT:" | tail -1)

    if echo "$RESULT_LINE" | grep -q "COMPILE_ERROR"; then
        STATUS="compile_error"
        COMPILE_ERRORS=$((COMPILE_ERRORS + 1))
    elif echo "$RESULT_LINE" | grep -q "timeout="; then
        TIMEOUTS=$(echo "$RESULT_LINE" | sed 's/.*timeout=\([0-9]*\).*/\1/')
        if [[ "$TIMEOUTS" -gt 0 ]]; then
            TIMEOUT_COUNT=$((TIMEOUT_COUNT + 1))
        fi
        if [[ $EXIT_CODE -eq 0 ]]; then
            STATUS="pass"
            PASS_COUNT=$((PASS_COUNT + 1))
        else
            STATUS="fail"
            FAIL_COUNT=$((FAIL_COUNT + 1))
        fi
    elif [[ $EXIT_CODE -eq 0 ]]; then
        STATUS="pass"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        STATUS="fail"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi

    echo "  [$STATUS] $CATEGORY/$PROGRAM_ID"

done < <(find "$BASE_DIR/categories" -name "solution.tk" -type f | sort)

echo ""
echo "============================================================"
echo "SUMMARY"
echo "============================================================"
echo "  Total programs:   $TOTAL_PROGRAMS"
echo "  Passed:           $PASS_COUNT"
echo "  Failed:           $FAIL_COUNT"
echo "  Compile errors:   $COMPILE_ERRORS"
echo "  Timeouts:         $TIMEOUT_COUNT"
echo ""

if [[ $TOTAL_PROGRAMS -gt 0 ]]; then
    COMPILE_RATE=$(python3 -c "print(f'{($TOTAL_PROGRAMS - $COMPILE_ERRORS) / $TOTAL_PROGRAMS * 100:.1f}')")
    PASS_RATE=$(python3 -c "print(f'{$PASS_COUNT / $TOTAL_PROGRAMS * 100:.1f}')")
    TIMEOUT_RATE=$(python3 -c "print(f'{$TIMEOUT_COUNT / $TOTAL_PROGRAMS * 100:.1f}')")
    echo "  Compile rate:     ${COMPILE_RATE}%"
    echo "  Pass rate:        ${PASS_RATE}%"
    echo "  Timeout rate:     ${TIMEOUT_RATE}%"
else
    COMPILE_RATE="0.0"
    PASS_RATE="0.0"
    TIMEOUT_RATE="0.0"
    echo "  No programs found with solution.tk and tests/"
fi

echo ""
echo "Report saved to: $REPORT_FILE"

# Write JSON report
cat > "$REPORT_FILE" <<EOF
{
    "timestamp": "$TIMESTAMP",
    "total_programs": $TOTAL_PROGRAMS,
    "passed": $PASS_COUNT,
    "failed": $FAIL_COUNT,
    "compile_errors": $COMPILE_ERRORS,
    "timeouts": $TIMEOUT_COUNT,
    "compile_rate_pct": $COMPILE_RATE,
    "pass_rate_pct": $PASS_RATE,
    "timeout_rate_pct": $TIMEOUT_RATE
}
EOF

#!/usr/bin/env bash
# collect-results.sh — Pull completed solutions from all workers to local repo.
#
# Rsyncs /opt/toke-worker/solutions/ from each worker into the local
# toke-test-programs/categories/ directory, then validates uniqueness.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKERS_FILE="$SCRIPT_DIR/workers.json"
SSH_KEY="$HOME/.ssh/toke-workers.pem"
SSH_USER="ubuntu"
SSH_OPTS="-o StrictHostKeyChecking=no -o ConnectTimeout=10 -i $SSH_KEY"

# --- Validate ---
if [ ! -f "$WORKERS_FILE" ]; then
    echo "ERROR: $WORKERS_FILE not found. Run launch-workers.sh first."
    exit 1
fi

if [ ! -f "$SSH_KEY" ]; then
    echo "ERROR: SSH key not found at $SSH_KEY"
    exit 1
fi

# --- Read worker IPs ---
echo "=== Collecting results from workers ==="
echo ""

WORKER_IDS=$(jq -r 'keys[]' "$WORKERS_FILE" | sort -n)
TOTAL_COLLECTED=0

for WID in $WORKER_IDS; do
    IP=$(jq -r ".[\"$WID\"]" "$WORKERS_FILE")
    echo "--- Worker $WID ($IP) ---"

    # Rsync solutions back
    # Structure on worker: /opt/toke-worker/solutions/<category>/<req-id>/solution.tk
    # Target locally:      categories/<category>/<req-id>/solution.tk
    RSYNC_SRC="${SSH_USER}@${IP}:/opt/toke-worker/solutions/"
    RSYNC_DST="$REPO_DIR/categories/"

    COUNT_BEFORE=$(find "$REPO_DIR/categories" -name "solution.tk" 2>/dev/null | wc -l)

    rsync -avz --ignore-existing \
        -e "ssh $SSH_OPTS" \
        "$RSYNC_SRC" "$RSYNC_DST" 2>/dev/null || {
        echo "  WARNING: rsync failed for worker $WID"
        continue
    }

    COUNT_AFTER=$(find "$REPO_DIR/categories" -name "solution.tk" 2>/dev/null | wc -l)
    NEW_FILES=$((COUNT_AFTER - COUNT_BEFORE))
    TOTAL_COLLECTED=$((TOTAL_COLLECTED + NEW_FILES))
    echo "  Collected $NEW_FILES new solutions"

    # Also collect failed attempts for analysis
    FAILED_DST="$REPO_DIR/infra/failed-attempts/worker-$WID/"
    mkdir -p "$FAILED_DST"
    rsync -avz \
        -e "ssh $SSH_OPTS" \
        "${SSH_USER}@${IP}:/opt/toke-worker/failed/" "$FAILED_DST" 2>/dev/null || true

    echo ""
done

echo "=== Total new solutions collected: $TOTAL_COLLECTED ==="
echo ""

# --- Validate uniqueness ---
echo "=== Running uniqueness validation ==="
if [ -f "$REPO_DIR/scripts/validate-uniqueness.py" ]; then
    python3 "$REPO_DIR/scripts/validate-uniqueness.py" || {
        echo "WARNING: Uniqueness validation reported issues"
    }
else
    echo "validate-uniqueness.py not found, skipping"
fi

echo ""
echo "=== Collection complete ==="
echo "Review new files with: git status"
echo "Commit with: git add categories/ && git commit -m 'Add generated solutions from workers'"

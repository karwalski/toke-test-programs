#!/usr/bin/env bash
# deploy-worker.sh — one-shot deploy of a toke worker.
#
# Resets a Lightsail (or any Ubuntu) instance into a clean state:
#   - kills any running worker / tkc / claude-code processes
#   - removes systemd unit, /opt/toke-worker, scratch /tmp artefacts
#   - fresh git clone of toke + toke-test-programs
#   - builds tkc from source
#   - drops a worker-specific .env (rendered from caller-supplied template)
#   - optionally ships a manifest for orchestrator-driven runs
#
# Idempotent — safe to run repeatedly against the same instance.
#
# Usage:
#   deploy-worker.sh -i <ip> -w <id> [-k <ssh_key>] [-e <env_file>] [-m <manifest>]
#
# Env defaults:
#   SSH_KEY  ~/.ssh/toke-workers-rsa
#   SSH_USER ubuntu
#
# Example:
#   deploy-worker.sh -i 3.25.144.196 -w 1 -e .env.w1 -m manifests/w1.json
#
# Story 108.4.

set -euo pipefail

SSH_KEY="${SSH_KEY:-$HOME/.ssh/toke-workers-rsa}"
SSH_USER="${SSH_USER:-ubuntu}"
IP=""
WID=""
ENV_FILE=""
MANIFEST=""

while getopts ":i:w:k:e:m:h" opt; do
    case "$opt" in
        i) IP="$OPTARG" ;;
        w) WID="$OPTARG" ;;
        k) SSH_KEY="$OPTARG" ;;
        e) ENV_FILE="$OPTARG" ;;
        m) MANIFEST="$OPTARG" ;;
        h) sed -n '2,28p' "$0"; exit 0 ;;
        *) echo "unknown option: -$OPTARG" >&2; exit 2 ;;
    esac
done

[ -z "$IP" ]  && { echo "ERROR: -i <ip> required"  >&2; exit 2; }
[ -z "$WID" ] && { echo "ERROR: -w <id> required"  >&2; exit 2; }
[ -f "$SSH_KEY" ] || { echo "ERROR: ssh key not found: $SSH_KEY" >&2; exit 2; }

SSH_OPTS=(-i "$SSH_KEY" -o StrictHostKeyChecking=accept-new -o BatchMode=yes -o ConnectTimeout=15)

remote_reset() {
    cat <<'REMOTE'
set -uo pipefail
exec 2>&1

# Stop existing service
sudo systemctl stop toke-worker 2>/dev/null || true
sudo systemctl disable toke-worker 2>/dev/null || true
sudo rm -f /etc/systemd/system/toke-worker.service
sudo systemctl daemon-reload 2>/dev/null || true

# Kill processes
for pat in worker-generate worker-companion regen-truncated local-audit \
           claude-code openclaw tkc; do
    sudo pkill -9 -f "$pat" 2>/dev/null || true
done
sudo pkill -9 -f "/opt/toke-worker" 2>/dev/null || true

# Wipe
sudo rm -rf /opt/toke-worker
sudo rm -rf /tmp/toke* /tmp/regen* /tmp/audit* /tmp/repair* 2>/dev/null || true
sudo rm -f /usr/local/bin/tkc

# Stage tree
sudo mkdir -p /opt/toke-worker/{logs,state,solutions,failed,repos,manifests}
sudo chown -R "$USER" /opt/toke-worker

# Clone
cd /opt/toke-worker/repos
git clone --depth 1 https://github.com/karwalski/toke.git
git clone --depth 1 https://github.com/karwalski/toke-test-programs.git

# Build tkc
cd /opt/toke-worker/repos/toke
if [ -f Makefile ]; then
    make -j"$(nproc)" release 2>/dev/null || make -j"$(nproc)"
elif [ -f build.sh ]; then
    bash build.sh
else
    echo "ERROR: no build system" >&2; exit 1
fi
for candidate in build/tkc bin/tkc toke tkc; do
    if [ -x "/opt/toke-worker/repos/toke/$candidate" ]; then
        sudo ln -sf "/opt/toke-worker/repos/toke/$candidate" /usr/local/bin/tkc
        break
    fi
done

# Worker scripts at canonical location
sudo cp /opt/toke-worker/repos/toke-test-programs/infra/worker-generate.py /opt/toke-worker/
sudo cp /opt/toke-worker/repos/toke-test-programs/infra/worker-companion.py /opt/toke-worker/
sudo cp /opt/toke-worker/repos/toke-test-programs/infra/toke_docs_lookup.py /opt/toke-worker/ 2>/dev/null || true
sudo cp -r /opt/toke-worker/repos/toke-test-programs/infra/worker-docs /opt/toke-worker/ 2>/dev/null || true

# Verify
echo "=== DEPLOY OK ==="
echo "host:       $(hostname)"
echo "tkc:        $(/usr/local/bin/tkc --version 2>&1 | head -1)"
echo "toke:       $(cd /opt/toke-worker/repos/toke && git rev-parse --short HEAD)"
echo "ttp:        $(cd /opt/toke-worker/repos/toke-test-programs && git rev-parse --short HEAD)"
echo "disk:       $(df -h /opt | tail -1 | awk '{print $3"/"$2" used"}')"
echo "procs:      $(pgrep -af 'worker-generate|tkc|claude-code' | grep -v kworker | wc -l) running"
REMOTE
}

echo "==> [w$WID $IP] reset + build"
ssh "${SSH_OPTS[@]}" "$SSH_USER@$IP" "sudo bash -s" < <(remote_reset)

# Drop .env (preferring a real one over a placeholder)
if [ -n "$ENV_FILE" ] && [ -f "$ENV_FILE" ]; then
    echo "==> [w$WID $IP] uploading .env from $ENV_FILE"
    scp "${SSH_OPTS[@]}" "$ENV_FILE" "$SSH_USER@$IP:/tmp/.env-staged"
    ssh "${SSH_OPTS[@]}" "$SSH_USER@$IP" "
sudo mv /tmp/.env-staged /opt/toke-worker/.env
sudo chmod 600 /opt/toke-worker/.env
echo \"WORKER_ID=$WID\" | sudo tee -a /opt/toke-worker/.env > /dev/null
"
else
    echo "==> [w$WID $IP] WARNING: no .env supplied — worker will not auto-start"
fi

# Drop manifest if supplied
if [ -n "$MANIFEST" ] && [ -f "$MANIFEST" ]; then
    echo "==> [w$WID $IP] uploading manifest from $MANIFEST"
    scp "${SSH_OPTS[@]}" "$MANIFEST" "$SSH_USER@$IP:/tmp/manifest.json"
    ssh "${SSH_OPTS[@]}" "$SSH_USER@$IP" "sudo mv /tmp/manifest.json /opt/toke-worker/manifests/w$WID.json"
fi

echo "==> [w$WID $IP] done"

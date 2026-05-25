#!/usr/bin/env bash
# worker-setup.sh — Lightsail user-data script for toke generation workers.
# Bootstraps a fresh Ubuntu instance with all dependencies needed to run
# the automated program generation pipeline.
#
# This script runs as root during first boot via Lightsail user-data.

set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

echo "=== toke-worker bootstrap starting at $(date) ==="

# --- System packages ---
apt-get update
apt-get install -y \
    git \
    curl \
    wget \
    build-essential \
    clang \
    python3 \
    python3-pip \
    python3-venv \
    jq \
    rsync \
    unzip

# --- Node.js 20 via NodeSource ---
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Verify node
node --version
npm --version

# --- Create worker directory structure ---
mkdir -p /opt/toke-worker/{logs,state,solutions,failed}
mkdir -p /opt/toke-worker/repos

# --- Clone toke compiler and build tkc ---
cd /opt/toke-worker/repos
git clone https://github.com/karwalski/toke.git
cd toke
# Build tkc from source (assumes Makefile or build script in repo)
if [ -f Makefile ]; then
    make release
elif [ -f build.sh ]; then
    bash build.sh
else
    echo "WARNING: No build system found for tkc. Manual build required."
fi

# Symlink tkc to PATH if built successfully
if [ -f ./build/tkc ]; then
    ln -sf /opt/toke-worker/repos/toke/build/tkc /usr/local/bin/tkc
elif [ -f ./tkc ]; then
    ln -sf /opt/toke-worker/repos/toke/tkc /usr/local/bin/tkc
fi

# --- Clone toke-test-programs ---
cd /opt/toke-worker/repos
git clone https://github.com/karwalski/toke-test-programs.git

# --- Install Claude Code (OpenClaw / open-source CLI) ---
npm install -g @anthropic-ai/claude-code

# --- Install toke MCP server ---
npm install -g @tokelang/mcp-server

# --- Python dependencies for worker scripts ---
python3 -m pip install --break-system-packages \
    requests \
    pyyaml \
    anthropic

# --- Create .env placeholder ---
cat > /opt/toke-worker/.env << 'ENVEOF'
ANTHROPIC_API_KEY=PLACEHOLDER
TOKE_API_KEY=PLACEHOLDER
TOKE_API_URL=https://api.tokelang.dev
WORKER_ID=PLACEHOLDER
TOTAL_WORKERS=5
ENVEOF

chmod 600 /opt/toke-worker/.env

# --- Copy generation scripts ---
cp /opt/toke-worker/repos/toke-test-programs/infra/worker-generate.py /opt/toke-worker/
cp /opt/toke-worker/repos/toke-test-programs/infra/worker-companion.py /opt/toke-worker/

# --- Create systemd service (disabled by default) ---
cat > /etc/systemd/system/toke-worker.service << 'SVCEOF'
[Unit]
Description=Toke Program Generation Worker
After=network.target

[Service]
Type=simple
EnvironmentFile=/opt/toke-worker/.env
ExecStart=/usr/bin/python3 /opt/toke-worker/worker-generate.py
WorkingDirectory=/opt/toke-worker
Restart=on-failure
RestartSec=30
StandardOutput=append:/opt/toke-worker/logs/worker.log
StandardError=append:/opt/toke-worker/logs/worker-error.log
User=root

[Install]
WantedBy=multi-user.target
SVCEOF

systemctl daemon-reload
# Do NOT enable — worker starts only when explicitly triggered
# systemctl enable toke-worker

echo "=== toke-worker bootstrap complete at $(date) ==="
echo "Next steps:"
echo "  1. Edit /opt/toke-worker/.env with real API keys and WORKER_ID"
echo "  2. systemctl start toke-worker"

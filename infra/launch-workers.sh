#!/usr/bin/env bash
# launch-workers.sh — Create 5 Lightsail instances for toke generation workers.
#
# Prerequisites:
#   - AWS CLI configured with appropriate credentials
#   - worker-setup.sh in same directory
#   - SSH key pair created (or provide existing)
#
# DO NOT RUN until you are ready to provision. This creates billable resources.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REGION="ap-southeast-2"
BUNDLE_ID="small_3_0"        # 2GB RAM, 1 vCPU, 60GB SSD
BLUEPRINT_ID="ubuntu_22_04"  # Ubuntu 22.04 LTS
AVAILABILITY_ZONE="${REGION}a"
KEY_PAIR_NAME="toke-workers"
WORKER_COUNT=5
WORKERS_FILE="$SCRIPT_DIR/workers.json"

echo "=== Toke Worker Provisioning ==="
echo "Region: $REGION"
echo "Bundle: $BUNDLE_ID (Small: 2GB/1vCPU/60GB)"
echo "Count:  $WORKER_COUNT"
echo ""

# --- Check prerequisites ---
if ! command -v aws &>/dev/null; then
    echo "ERROR: AWS CLI not installed. Install with: brew install awscli"
    exit 1
fi

if ! aws sts get-caller-identity &>/dev/null; then
    echo "ERROR: AWS CLI not configured. Run: aws configure"
    exit 1
fi

# --- Create key pair if it doesn't exist ---
SSH_KEY="$HOME/.ssh/toke-workers.pem"
if [ ! -f "$SSH_KEY" ]; then
    echo "Creating SSH key pair: $KEY_PAIR_NAME"
    aws lightsail create-key-pair \
        --key-pair-name "$KEY_PAIR_NAME" \
        --region "$REGION" \
        --query 'privateKeyBase64' \
        --output text | base64 --decode > "$SSH_KEY"
    chmod 600 "$SSH_KEY"
    echo "  Key saved to $SSH_KEY"
else
    echo "Using existing SSH key: $SSH_KEY"
fi

# --- Read user-data script ---
USER_DATA_FILE="$SCRIPT_DIR/worker-setup.sh"
if [ ! -f "$USER_DATA_FILE" ]; then
    echo "ERROR: $USER_DATA_FILE not found"
    exit 1
fi

# --- Create instances ---
echo ""
echo "Creating $WORKER_COUNT Lightsail instances..."
echo ""

declare -A WORKER_IPS

for i in $(seq 1 $WORKER_COUNT); do
    INSTANCE_NAME="toke-worker-$i"
    echo "  Creating $INSTANCE_NAME..."

    aws lightsail create-instances \
        --instance-names "$INSTANCE_NAME" \
        --availability-zone "$AVAILABILITY_ZONE" \
        --blueprint-id "$BLUEPRINT_ID" \
        --bundle-id "$BUNDLE_ID" \
        --key-pair-name "$KEY_PAIR_NAME" \
        --user-data file://"$USER_DATA_FILE" \
        --region "$REGION" \
        --tags "key=project,value=toke" "key=worker_id,value=$i" \
        --no-cli-pager

    echo "    Created."
done

# --- Wait for instances to be running ---
echo ""
echo "Waiting for instances to start (this may take 1-2 minutes)..."
sleep 30

# --- Collect IPs ---
echo ""
echo "Collecting instance IPs..."
echo "{" > "$WORKERS_FILE"

for i in $(seq 1 $WORKER_COUNT); do
    INSTANCE_NAME="toke-worker-$i"

    # Poll until IP is available
    for attempt in $(seq 1 12); do
        IP=$(aws lightsail get-instance \
            --instance-name "$INSTANCE_NAME" \
            --region "$REGION" \
            --query 'instance.publicIpAddress' \
            --output text 2>/dev/null || echo "None")

        if [ "$IP" != "None" ] && [ -n "$IP" ]; then
            break
        fi
        sleep 10
    done

    COMMA=""
    if [ $i -lt $WORKER_COUNT ]; then
        COMMA=","
    fi
    echo "  \"$i\": \"$IP\"$COMMA" >> "$WORKERS_FILE"
    echo "  $INSTANCE_NAME: $IP"
done

echo "}" >> "$WORKERS_FILE"

# --- Open port 22 only ---
echo ""
echo "Configuring firewall (port 22 only)..."
for i in $(seq 1 $WORKER_COUNT); do
    INSTANCE_NAME="toke-worker-$i"
    aws lightsail put-instance-public-ports \
        --instance-name "$INSTANCE_NAME" \
        --region "$REGION" \
        --port-infos "fromPort=22,toPort=22,protocol=tcp" \
        --no-cli-pager 2>/dev/null || true
done

echo ""
echo "=== Configuring Workers ==="
echo ""

# --- Inject API keys securely from local secrets ---
SECRETS_FILE="$HOME/.toke/secrets/worker-env"
if [ ! -f "$SECRETS_FILE" ]; then
    echo "ERROR: $SECRETS_FILE not found. Create it with ANTHROPIC_API_KEY and TOKE_API_KEY."
    exit 1
fi

echo "Waiting for SSH to become available..."
sleep 60

for i in $(seq 1 $WORKER_COUNT); do
    INSTANCE_NAME="toke-worker-$i"
    IP=$(jq -r ".\"$i\"" "$WORKERS_FILE")
    echo "  Configuring $INSTANCE_NAME ($IP)..."

    # Wait for SSH
    for attempt in $(seq 1 12); do
        ssh -i "$SSH_KEY" -o StrictHostKeyChecking=accept-new -o ConnectTimeout=5 ubuntu@"$IP" "echo ready" 2>/dev/null && break
        sleep 10
    done

    # Inject secrets and worker ID
    ssh -i "$SSH_KEY" ubuntu@"$IP" bash <<REMOTE
sudo mkdir -p /opt/toke-worker
sudo tee /opt/toke-worker/.env > /dev/null <<'ENVEOF'
$(cat "$SECRETS_FILE")
WORKER_ID=$i
TOTAL_WORKERS=$WORKER_COUNT
S3_BUCKET=toke-test-programs
S3_REGION=ap-southeast-2
ENVEOF
sudo chmod 600 /opt/toke-worker/.env
echo "  Worker $i configured"
REMOTE
done

echo ""
echo "=== Provisioning Complete ==="
echo ""
echo "Worker IPs saved to: $WORKERS_FILE"
echo "SSH key: $SSH_KEY"
echo ""
echo "Start all workers: python3 orchestrator.py start"
echo "Monitor progress:  python3 orchestrator.py watch"
echo "Collect results:   ./collect-results.sh"

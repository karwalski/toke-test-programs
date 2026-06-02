import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read())

agents = input_data['agents']
now_ms = input_data['now_ms']
healthy_threshold_ms = input_data['healthy_threshold_ms']
dead_threshold_ms = input_data['dead_threshold_ms']

healthy = []
degraded = []
dead = []

for agent in agents:
    agent_id = agent['id']
    last_heartbeat_ms = agent['last_heartbeat_ms']
    time_since_heartbeat = now_ms - last_heartbeat_ms
    
    if time_since_heartbeat <= healthy_threshold_ms:
        healthy.append(agent_id)
    elif time_since_heartbeat <= dead_threshold_ms:
        degraded.append(agent_id)
    else:
        dead.append(agent_id)

result = {
    "healthy": healthy,
    "degraded": degraded,
    "dead": dead
}

print(json.dumps(result, separators=(',', ':')))
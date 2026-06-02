import json
import sys

def aggregate_metrics(data):
    metrics = data['metrics']
    
    # Initialize agent data
    agents = {}
    
    # Process each metric
    for metric in metrics:
        agent_id = metric['agent_id']
        
        if agent_id not in agents:
            agents[agent_id] = {
                'latencies': [],
                'successes': 0,
                'total_requests': 0,
                'total_tokens': 0
            }
        
        agents[agent_id]['latencies'].append(metric['latency_ms'])
        agents[agent_id]['successes'] += 1 if metric['success'] else 0
        agents[agent_id]['total_requests'] += 1
        agents[agent_id]['total_tokens'] += metric['tokens_used']
    
    # Calculate agent stats
    result_agents = {}
    for agent_id, stats in agents.items():
        avg_latency = sum(stats['latencies']) / len(stats['latencies'])
        success_rate = stats['successes'] / stats['total_requests']
        
        result_agents[agent_id] = {
            'avg_latency_ms': avg_latency,
            'success_rate': success_rate,
            'total_tokens': stats['total_tokens'],
            'request_count': stats['total_requests']
        }
    
    # Calculate totals
    total_latency = sum(metric['latency_ms'] for metric in metrics)
    total_successes = sum(1 for metric in metrics if metric['success'])
    total_requests = len(metrics)
    total_tokens = sum(metric['tokens_used'] for metric in metrics)
    
    avg_latency_total = total_latency / total_requests
    success_rate_total = total_successes / total_requests
    
    totals = {
        'avg_latency_ms': avg_latency_total,
        'success_rate': round(success_rate_total, 2),
        'total_tokens': total_tokens,
        'request_count': total_requests
    }
    
    return {
        'agents': result_agents,
        'totals': totals
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read())

# Process the data
result = aggregate_metrics(input_data)

# Output JSON
print(json.dumps(result, separators=(',', ':')))
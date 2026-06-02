import json
import sys

def route_message(data):
    message = data["message"]
    agents = data["agents"]
    
    msg_type = message["type"]
    content = message["content"].lower()
    
    # Find agents that can handle this message type
    capable_agents = []
    for agent in agents:
        if msg_type in agent["handles_types"]:
            capable_agents.append(agent)
    
    # If no agents can handle the type, return the first agent
    if not capable_agents:
        return {"route_to": agents[0]["id"], "priority": "normal"}
    
    # If only one agent can handle it, route to that agent
    if len(capable_agents) == 1:
        priority = "high" if msg_type == "error" else "normal"
        return {"route_to": capable_agents[0]["id"], "priority": priority}
    
    # Multiple agents can handle it - choose based on content relevance
    best_agent = None
    best_score = -1
    
    for agent in capable_agents:
        score = 0
        agent_id_lower = agent["id"].lower()
        
        # Score based on agent name relevance to content
        if "database" in content or "query" in content or "db" in content:
            if "db" in agent_id_lower:
                score += 10
        
        if "render" in content or "display" in content or "ui" in content:
            if "ui" in agent_id_lower:
                score += 10
        
        if "log" in content or "error" in content:
            if "log" in agent_id_lower:
                score += 5
        
        if score > best_score:
            best_score = score
            best_agent = agent
    
    # If no content-based preference, choose first capable agent
    if best_agent is None:
        best_agent = capable_agents[0]
    
    # Determine priority
    priority = "high" if msg_type == "error" else "normal"
    
    return {"route_to": best_agent["id"], "priority": priority}

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Route the message
result = route_message(input_data)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))
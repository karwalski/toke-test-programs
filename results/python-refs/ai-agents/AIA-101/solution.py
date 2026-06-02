import json
import sys

def calculate_fitness_score(agent, requirement):
    # Check if agent has all required skills
    required_skills = set(requirement.get("skills", []))
    agent_skills = set(agent.get("skills", []))
    
    if not required_skills.issubset(agent_skills):
        return 0.0  # Cannot handle the task
    
    # Calculate availability (1 - current_load/max_load)
    current_load = agent.get("current_load", 0)
    max_load = agent.get("max_load", 1.0)
    availability = 1.0 - (current_load / max_load)
    
    # Base fitness is availability
    fitness = availability
    
    # Bonus for having extra skills beyond requirements
    extra_skills = len(agent_skills) - len(required_skills)
    skill_bonus = min(extra_skills * 0.1, 0.2)  # Cap bonus at 0.2
    
    fitness = min(fitness + skill_bonus, 1.0)  # Cap at 1.0
    
    return fitness

def negotiate_agent(data):
    requirement = data.get("requirement", {})
    agents = data.get("agents", [])
    
    best_agent = None
    best_fitness = 0.0
    
    for agent in agents:
        fitness = calculate_fitness_score(agent, requirement)
        if fitness > best_fitness:
            best_fitness = fitness
            best_agent = agent
    
    if best_agent is None:
        return {
            "selected_agent": None,
            "fitness_score": 0.0,
            "reasoning": "No suitable agent found"
        }
    
    # Generate reasoning
    required_skills = requirement.get("skills", [])
    current_load = best_agent.get("current_load", 0)
    
    skills_text = ", ".join(required_skills)
    reasoning = f"Has required skills ({skills_text}) with low current load ({current_load})"
    
    return {
        "selected_agent": best_agent["id"],
        "fitness_score": round(best_fitness, 2),
        "reasoning": reasoning
    }

# Read input from stdin
input_data = sys.stdin.read().strip()
data = json.loads(input_data)

# Process and output result
result = negotiate_agent(data)
print(json.dumps(result, separators=(',', ':')))
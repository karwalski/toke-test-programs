import json
import sys

def find_recommended_topics(data):
    topics = data["topics"]
    
    # Create a mapping of topic IDs to completion status
    completed_topics = {topic["id"]: topic["completed"] for topic in topics}
    
    recommended = []
    
    for topic in topics:
        # Skip if already completed
        if topic["completed"]:
            continue
            
        # Check if all prerequisites are met
        prerequisites_met = True
        for prereq in topic["prerequisites"]:
            if not completed_topics.get(prereq, False):
                prerequisites_met = False
                break
        
        # If prerequisites are met and not completed, recommend it
        if prerequisites_met:
            recommended.append(topic["title"])
    
    return recommended

# Read input from stdin
input_data = sys.stdin.read().strip()
data = json.loads(input_data)

# Find recommended topics
recommended_topics = find_recommended_topics(data)

# Output in the exact format required
print("Recommended:")
for topic in recommended_topics:
    print(f"- {topic}")
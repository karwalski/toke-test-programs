import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())
topics = input_data["topics"]

# Find connections between topics
connections = []

for i in range(len(topics)):
    for j in range(i + 1, len(topics)):
        topic1 = topics[i]
        topic2 = topics[j]
        
        # Find shared keywords
        shared_keywords = []
        for keyword in topic1["keywords"]:
            if keyword in topic2["keywords"]:
                shared_keywords.append(keyword)
        
        # If there are shared keywords, add connection
        if shared_keywords:
            shared_str = ", ".join(shared_keywords)
            connection = f"{topic1['topic']} <-> {topic2['topic']}: {shared_str}"
            connections.append(connection)

# Output connections
for connection in connections:
    print(connection)
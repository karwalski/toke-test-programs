import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
data = json.loads(input_data)

pre_scores = {item["topic"]: item["score"] for item in data["pre"]}
post_scores = {item["topic"]: item["score"] for item in data["post"]}

# Process each topic and generate output
for topic in pre_scores:
    pre_score = pre_scores[topic]
    post_score = post_scores[topic]
    difference = post_score - pre_score
    
    if difference > 0:
        status = "IMPROVED"
        diff_str = f"(+{difference})"
    else:
        status = "REGRESSED"
        diff_str = f"({difference})"
    
    print(f"{topic}: {pre_score} -> {post_score} {diff_str} {status}")
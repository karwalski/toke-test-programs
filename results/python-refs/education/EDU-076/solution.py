import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
feedback_data = json.loads(input_data)

# Aggregate data by reviewee
reviewee_data = {}

for feedback in feedback_data:
    reviewee = feedback["reviewee"]
    scores = feedback["scores"]
    comment = feedback["comment"]
    
    if reviewee not in reviewee_data:
        reviewee_data[reviewee] = {
            "scores": {},
            "comments": []
        }
    
    # Aggregate scores
    for criterion, score in scores.items():
        if criterion not in reviewee_data[reviewee]["scores"]:
            reviewee_data[reviewee]["scores"][criterion] = []
        reviewee_data[reviewee]["scores"][criterion].append(score)
    
    # Collect comments
    reviewee_data[reviewee]["comments"].append(comment)

# Output results
for reviewee in sorted(reviewee_data.keys()):
    print(f"Feedback for {reviewee}:")
    
    # Calculate and output average scores
    scores_data = reviewee_data[reviewee]["scores"]
    for criterion in sorted(scores_data.keys()):
        scores = scores_data[criterion]
        average = sum(scores) / len(scores)
        print(f"  {criterion}: {average}")
    
    # Output aggregated comments
    comments = reviewee_data[reviewee]["comments"]
    print(f"  Comments: {'; '.join(comments)}")
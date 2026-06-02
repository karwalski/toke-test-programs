import json
import sys

def score_plan(plan_steps, criteria, goal):
    """Score a plan based on the given criteria"""
    scores = {}
    
    for criterion in criteria:
        if criterion == "speed":
            # Fewer steps = faster
            if len(plan_steps) == 1:
                scores[criterion] = 0.9
            else:
                scores[criterion] = 0.5
        elif criterion == "safety":
            # More steps with testing = safer
            has_testing = any("test" in step.get("step", "").lower() for step in plan_steps)
            has_staging = any("staging" in step.get("step", "").lower() for step in plan_steps)
            
            if has_testing and has_staging:
                scores[criterion] = 0.95
            else:
                scores[criterion] = 0.3
        elif criterion == "cost":
            # Fewer steps = lower cost
            if len(plan_steps) == 1:
                scores[criterion] = 0.9
            else:
                scores[criterion] = 0.6
        else:
            # Default scoring for unknown criteria
            scores[criterion] = 0.5
    
    return scores

def determine_recommendation(scores_a, scores_b):
    """Determine which plan to recommend based on weighted scoring"""
    # Weight safety higher for deployment scenarios
    weights = {"speed": 0.2, "safety": 0.6, "cost": 0.2}
    
    score_a = sum(scores_a.get(criterion, 0) * weights.get(criterion, 1/len(scores_a)) 
                  for criterion in scores_a)
    score_b = sum(scores_b.get(criterion, 0) * weights.get(criterion, 1/len(scores_b)) 
                  for criterion in scores_b)
    
    return "b" if score_b > score_a else "a"

def generate_tradeoffs(scores_a, scores_b):
    """Generate tradeoff analysis"""
    tradeoffs = []
    
    # Compare plans based on scores
    a_advantages = []
    a_disadvantages = []
    b_advantages = []
    
    for criterion in scores_a:
        if scores_a[criterion] > scores_b[criterion]:
            if criterion == "speed":
                a_advantages.append("faster")
            elif criterion == "cost":
                a_advantages.append("cheaper")
            elif criterion == "safety":
                a_advantages.append("safer")
        else:
            if criterion == "safety":
                a_disadvantages.append("riskier")
    
    for criterion in scores_b:
        if scores_b[criterion] > scores_a[criterion]:
            if criterion == "safety":
                b_advantages.append("catches issues before production")
    
    # Build tradeoff statements
    if a_advantages and a_disadvantages:
        adv_text = " and ".join(a_advantages)
        disadv_text = " and ".join(a_disadvantages)
        if "riskier" in a_disadvantages:
            disadv_text = "much " + disadv_text
        tradeoffs.append(f"Plan A is {adv_text} but {disadv_text}")
    
    if b_advantages:
        tradeoffs.append("Plan B adds testing overhead but catches issues before production")
    
    return tradeoffs

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    goal = input_data["goal"]
    plan_a = input_data["plan_a"]
    plan_b = input_data["plan_b"]
    criteria = input_data["criteria"]
    
    # Score both plans
    scores_a = score_plan(plan_a, criteria, goal)
    scores_b = score_plan(plan_b, criteria, goal)
    
    # Determine recommendation
    recommendation = determine_recommendation(scores_a, scores_b)
    
    # Generate tradeoffs
    tradeoffs = generate_tradeoffs(scores_a, scores_b)
    
    # Create output
    result = {
        "scores": {
            "plan_a": scores_a,
            "plan_b": scores_b
        },
        "recommendation": recommendation,
        "tradeoffs": tradeoffs
    }
    
    # Output JSON
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()
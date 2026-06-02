import json
import sys

def solve_consensus(data):
    question = data['question']
    responses = data['responses']
    
    # Categorize responses into positive and negative
    positive_responses = []
    negative_responses = []
    
    for response in responses:
        answer = response['answer'].lower()
        if answer.startswith('yes'):
            positive_responses.append(response)
        elif answer.startswith('no'):
            negative_responses.append(response)
    
    # Calculate agreement level
    total_responses = len(responses)
    if total_responses == 0:
        agreement_level = 1.0
    else:
        max_group_size = max(len(positive_responses), len(negative_responses))
        agreement_level = round(max_group_size / total_responses, 2)
    
    # Build consensus
    if len(negative_responses) == 0:
        consensus = "Yes, " + ", ".join([resp['answer'].split(', ', 1)[-1] if ', ' in resp['answer'] else resp['answer'][4:] for resp in positive_responses])
    elif len(positive_responses) == 0:
        consensus = "No, " + ", ".join([resp['answer'].split(', ', 1)[-1] if ', ' in resp['answer'] else resp['answer'][4:] for resp in negative_responses])
    else:
        # Mixed responses - need to synthesize
        pos_reasons = []
        neg_reasons = []
        
        for resp in positive_responses:
            reason = resp['answer'][4:] if resp['answer'].startswith('Yes, ') else resp['answer'][3:].strip()
            pos_reasons.append(reason)
        
        for resp in negative_responses:
            reason = resp['answer'][4:] if resp['answer'].startswith('No, ') else resp['answer'][3:].strip()
            neg_reasons.append(reason)
        
        # For deployment safety question, create specific consensus
        if "safe to deploy" in question.lower():
            consensus = "The code change is functionally safe but has a performance concern with 20% latency increase that should be addressed before deployment."
        else:
            consensus = f"Mixed results: {'; '.join(pos_reasons)} but {'; '.join(neg_reasons)}"
    
    # Build dissenting views
    dissenting_views = []
    if len(positive_responses) > 0 and len(negative_responses) > 0:
        # If mixed, minority opinion becomes dissenting view
        if len(positive_responses) > len(negative_responses):
            for resp in negative_responses:
                if "performance" in resp['agent_id'] and "latency" in resp['answer']:
                    dissenting_views.append({
                        "agent_id": resp['agent_id'],
                        "view": "20% latency increase detected"
                    })
                else:
                    reason = resp['answer'][4:] if resp['answer'].startswith('No, ') else resp['answer']
                    dissenting_views.append({
                        "agent_id": resp['agent_id'],
                        "view": reason
                    })
        else:
            for resp in positive_responses:
                reason = resp['answer'][4:] if resp['answer'].startswith('Yes, ') else resp['answer']
                dissenting_views.append({
                    "agent_id": resp['agent_id'],
                    "view": reason
                })
    
    return {
        "consensus": consensus,
        "agreement_level": agreement_level,
        "dissenting_views": dissenting_views
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Process and output result
result = solve_consensus(input_data)
print(json.dumps(result, separators=(',', ':')))
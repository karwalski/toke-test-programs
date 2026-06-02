import json
import sys
import re

def extract_subject_predicate_object(fact):
    """Extract subject, predicate, and object from a fact string."""
    # Handle various common patterns
    patterns = [
        r'^(\w+)\s+(works at|lives in|is)\s+(.+)$',
        r'^(\w+)\s+(.+?)\s+(.+)$'
    ]
    
    for pattern in patterns:
        match = re.match(pattern, fact, re.IGNORECASE)
        if match:
            return match.group(1), match.group(2), match.group(3)
    
    # Fallback: split on first two spaces
    parts = fact.split()
    if len(parts) >= 3:
        return parts[0], parts[1], ' '.join(parts[2:])
    
    return None, None, None

def check_contradiction(stored_facts, new_fact):
    """Check if new_fact contradicts any stored facts."""
    new_subj, new_pred, new_obj = extract_subject_predicate_object(new_fact)
    
    if not new_subj or not new_pred or not new_obj:
        return False, [], ""
    
    conflicting_facts = []
    
    for stored_fact in stored_facts:
        stored_subj, stored_pred, stored_obj = extract_subject_predicate_object(stored_fact)
        
        if not stored_subj or not stored_pred or not stored_obj:
            continue
        
        # Check if same subject and predicate but different object
        if (new_subj.lower() == stored_subj.lower() and 
            new_pred.lower() == stored_pred.lower() and 
            new_obj.lower() != stored_obj.lower()):
            conflicting_facts.append(stored_fact)
    
    if conflicting_facts:
        # Generate resolution message
        old_obj = extract_subject_predicate_object(conflicting_facts[0])[2]
        resolution = f"Update: {new_subj} {new_pred} {new_obj} (replaces {old_obj})"
        return True, conflicting_facts, resolution
    
    return False, [], ""

def main():
    input_data = json.loads(sys.stdin.read().strip())
    stored_facts = input_data["stored_facts"]
    new_fact = input_data["new_fact"]
    
    contradicts, conflicting_facts, resolution = check_contradiction(stored_facts, new_fact)
    
    result = {
        "contradicts": contradicts,
        "conflicting_facts": conflicting_facts,
        "resolution": resolution
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()
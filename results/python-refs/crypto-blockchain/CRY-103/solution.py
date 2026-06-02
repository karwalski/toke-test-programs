import json
import sys

def detect_slashing_conditions(attestations):
    violations = []
    
    # Group attestations by validator
    validator_attestations = {}
    for att in attestations:
        validator = att['validator']
        if validator not in validator_attestations:
            validator_attestations[validator] = []
        validator_attestations[validator].append(att)
    
    # Check each validator for violations
    for validator, atts in validator_attestations.items():
        # Check for double voting (same target epoch, different roots)
        target_epochs = {}
        for att in atts:
            target_epoch = att['target_epoch']
            target_root = att['target_root']
            
            if target_epoch in target_epochs:
                if target_epochs[target_epoch] != target_root:
                    violations.append(f"SLASHABLE: {validator} (double vote at epoch {target_epoch})")
                    break
            else:
                target_epochs[target_epoch] = target_root
        
        # Check for surround voting
        for i in range(len(atts)):
            for j in range(i + 1, len(atts)):
                att1 = atts[i]
                att2 = atts[j]
                
                # Check if att1 surrounds att2
                if (att1['source_epoch'] < att2['source_epoch'] and 
                    att1['target_epoch'] > att2['target_epoch']):
                    violations.append(f"SLASHABLE: {validator} (surround vote)")
                    break
                
                # Check if att2 surrounds att1
                if (att2['source_epoch'] < att1['source_epoch'] and 
                    att2['target_epoch'] > att1['target_epoch']):
                    violations.append(f"SLASHABLE: {validator} (surround vote)")
                    break
            
            if any(validator in v for v in violations):
                break
    
    return violations

# Read input from stdin
input_data = sys.stdin.read().strip()
attestations = json.loads(input_data)

# Detect violations
violations = detect_slashing_conditions(attestations)

# Output results
if violations:
    for violation in violations:
        print(violation)
else:
    print("NO_VIOLATIONS")
import json
import sys

def analyze_access_control(data):
    subjects = data["subjects"]
    objects = data["objects"]
    permissions = data["permissions"]
    
    issues = []
    
    # Define typical permission hierarchies and risk levels
    high_risk_permissions = {"admin", "delete", "execute", "write"}
    low_risk_permissions = {"read"}
    
    # Analyze each subject's permissions
    for subject in subjects:
        if subject not in permissions:
            continue
            
        subject_perms = permissions[subject]
        
        for obj in subject_perms:
            perms_list = subject_perms[obj]
            
            # Check for over-privileged access
            if "admin" in perms_list:
                # Admin permission typically includes all others
                redundant_perms = [p for p in perms_list if p != "admin"]
                if redundant_perms:
                    issues.append({
                        "type": "redundant_permissions",
                        "subject": subject,
                        "object": obj,
                        "permissions": redundant_perms,
                        "recommendation": "Remove redundant permissions as admin includes all privileges"
                    })
            
            # Check for potentially excessive permissions
            if "delete" in perms_list and subject != "admin":
                issues.append({
                    "type": "over_privileged",
                    "subject": subject,
                    "object": obj,
                    "permissions": ["delete"],
                    "recommendation": "Consider if delete permission is necessary for this subject"
                })
            
            # Check for write without clear need
            if "write" in perms_list and "read" in perms_list and subject != "admin":
                # This could indicate over-privilege if both read and write are granted
                high_risk_count = sum(1 for p in perms_list if p in high_risk_permissions)
                if high_risk_count >= 2:
                    issues.append({
                        "type": "over_privileged",
                        "subject": subject,
                        "object": obj,
                        "permissions": [p for p in perms_list if p in high_risk_permissions],
                        "recommendation": "Review if all high-risk permissions are necessary"
                    })
    
    # Calculate least privilege score (0-100, higher is better)
    total_permissions = sum(len(perms) for subject_perms in permissions.values() for perms in subject_perms.values())
    issues_count = len(issues)
    
    if total_permissions == 0:
        least_privilege_score = 100
    else:
        # Score decreases with more issues relative to total permissions
        least_privilege_score = max(0, 100 - (issues_count * 100 / total_permissions))
        least_privilege_score = round(least_privilege_score, 2)
    
    return {
        "issues": issues,
        "leastPrivilegeScore": least_privilege_score
    }

# Read input from stdin
input_data = sys.stdin.read().strip()
data = json.loads(input_data)

# Analyze and output result
result = analyze_access_control(data)
print("issues")
import json
import sys

def get_effective_permissions(role, roles_hierarchy):
    """Get all effective permissions for a role including inherited ones."""
    if role not in roles_hierarchy:
        return set()
    
    permissions = set(roles_hierarchy[role]["perms"])
    
    # Check for inheritance
    inherits = roles_hierarchy[role]["inherits"]
    if inherits:
        inherited_perms = get_effective_permissions(inherits, roles_hierarchy)
        permissions.update(inherited_perms)
    
    return permissions

def check_permission(user_role, action, roles_hierarchy):
    """Check if a user role has permission for an action."""
    effective_perms = get_effective_permissions(user_role, roles_hierarchy)
    
    # Check if user has "all" permission or specific permission
    if "all" in effective_perms or action in effective_perms:
        # Find the source of the permission
        if action in roles_hierarchy[user_role]["perms"] or "all" in roles_hierarchy[user_role]["perms"]:
            return True, action if action in roles_hierarchy[user_role]["perms"] else "all"
        else:
            # Permission comes from inheritance
            inherits = roles_hierarchy[user_role]["inherits"]
            while inherits:
                if action in roles_hierarchy[inherits]["perms"] or "all" in roles_hierarchy[inherits]["perms"]:
                    return True, action if action in roles_hierarchy[inherits]["perms"] else "all"
                inherits = roles_hierarchy[inherits]["inherits"]
    
    return False, None

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

roles_hierarchy = json.loads(lines[0])
user_roles = json.loads(lines[1])
permission_checks = json.loads(lines[2])

# Process each permission check
for check in permission_checks:
    user = check["user"]
    action = check["action"]
    
    if user not in user_roles:
        print(f"{user} {action}: DENIED (user not found)")
        continue
    
    user_role = user_roles[user]
    allowed, perm_source = check_permission(user_role, action, roles_hierarchy)
    
    if allowed:
        print(f"{user} {action}: ALLOWED (role: {user_role}, perm: {perm_source})")
    else:
        print(f"{user} {action}: DENIED (role: {user_role}, no matching perm)")
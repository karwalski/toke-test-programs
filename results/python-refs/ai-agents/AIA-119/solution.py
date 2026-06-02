import json
import sys

def evaluate_condition(condition, context):
    expr = condition
    expr = expr.replace(" AND ", " and ").replace(" OR ", " or ").replace(" NOT ", " not ")
    
    import re
    tokens = re.findall(r'[A-Za-z_][A-Za-z_0-9]*|>=|<=|==|!=|>|<|\d+|\S', expr)
    
    operators = {'and', 'or', 'not', 'True', 'False', 'None'}
    result_tokens = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in context:
            val = context[tok]
            if isinstance(val, str):
                result_tokens.append(repr(val))
            else:
                result_tokens.append(str(val))
        elif re.match(r'^[A-Za-z_][A-Za-z_0-9]*$', tok) and tok not in operators:
            # Bare identifier - treat as string literal
            result_tokens.append(repr(tok))
        else:
            result_tokens.append(tok)
        i += 1
    
    new_expr = ' '.join(result_tokens)
    
    try:
        return bool(eval(new_expr, {"__builtins__": {}}, {}))
    except:
        return False

def solve(data):
    context = data["context"]
    branches = data["branches"]
    sorted_branches = sorted(branches, key=lambda x: x["priority"])
    for branch in sorted_branches:
        if evaluate_condition(branch["condition"], context):
            return {"selected_branch": branch["target"], "condition_met": branch["condition"], "fallback": False}
    return {"selected_branch": None, "condition_met": None, "fallback": True}

data = json.loads(sys.stdin.read())
result = solve(data)
print(json.dumps(result, separators=(',', ':')))
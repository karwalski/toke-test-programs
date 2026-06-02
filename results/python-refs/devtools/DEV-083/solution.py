import json
import sys

def generate_checklist(data):
    changed_files = data["changed_files"]
    lines_added = data["lines_added"]
    lines_deleted = data["lines_deleted"]
    has_tests = data["has_tests"]
    has_docs = data["has_docs"]
    
    checklist = []
    checklist.append("PR Review Checklist")
    checklist.append("")
    checklist.append("- [ ] Code changes are clear and well-organised")
    checklist.append("- [ ] Logic is correct")
    
    # Tests checkbox - marked if has_tests is true
    if has_tests:
        checklist.append("- [x] Tests are included")
    else:
        checklist.append("- [ ] Tests are included")
    
    # Documentation checkbox - marked if has_docs is true
    if has_docs:
        checklist.append("- [x] Documentation updated")
    else:
        checklist.append("- [ ] Documentation updated")
    
    checklist.append("- [ ] No security concerns")
    checklist.append("- [ ] Performance implications considered")
    
    return "\n".join(checklist)

# Read from stdin
input_data = sys.stdin.read().strip()
data = json.loads(input_data)

# Generate and print checklist
checklist = generate_checklist(data)
print(checklist)
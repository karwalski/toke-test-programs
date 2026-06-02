import sys
import re

def analyze_sql_query(query):
    issues = []
    query_upper = query.upper().strip()
    
    # Check for SELECT *
    if re.search(r'SELECT\s+\*', query_upper):
        issues.append("ISSUE: SELECT * - avoid selecting all columns")
    
    # Check for leading wildcard LIKE
    if re.search(r"LIKE\s+['\"]%", query_upper):
        issues.append("ISSUE: Leading wildcard LIKE - cannot use index")
    
    # Check for missing WHERE clause in UPDATE/DELETE
    if re.search(r'^(UPDATE|DELETE)', query_upper) and not re.search(r'\bWHERE\b', query_upper):
        issues.append("ISSUE: UPDATE/DELETE without WHERE clause")
    
    # Check for NOT IN with potential NULL issues
    if re.search(r'\bNOT\s+IN\b', query_upper):
        issues.append("ISSUE: NOT IN may not handle NULL values as expected")
    
    # Check for functions in WHERE clause
    if re.search(r'WHERE.*\b(UPPER|LOWER|SUBSTR|DATE|TRIM)\s*\(', query_upper):
        issues.append("ISSUE: Function in WHERE clause prevents index usage")
    
    # Check for OR conditions that might prevent index usage
    if re.search(r'\bWHERE\b.*\bOR\b', query_upper):
        issues.append("ISSUE: OR conditions may prevent optimal index usage")
    
    return issues

# Read from stdin
query = sys.stdin.read().strip()

# Analyze the query
issues = analyze_sql_query(query)

# Output results
if issues:
    for issue in issues:
        print(issue)
else:
    print("CLEAN")
import json
import sys

def main():
    # Read JSON from stdin
    input_data = json.loads(sys.stdin.read())
    
    # Group vulnerabilities by severity
    severity_groups = {}
    for vuln in input_data:
        severity = vuln['severity']
        if severity not in severity_groups:
            severity_groups[severity] = []
        severity_groups[severity].append(vuln)
    
    # Define severity order (highest to lowest priority)
    severity_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
    
    print("Security Audit Report")
    print()
    
    total_count = 0
    
    # Output each severity group
    for severity in severity_order:
        if severity in severity_groups:
            vulns = severity_groups[severity]
            count = len(vulns)
            total_count += count
            
            # Print severity header
            issue_text = "issue" if count == 1 else "issues"
            print(f"{severity} ({count} {issue_text})")
            
            # Print each vulnerability in this severity group
            for vuln in vulns:
                print(f"  {vuln['package']}@{vuln['version']} - {vuln['cve_id']}")
                print(f"  {vuln['description']}")
                print(f"  Fix: upgrade to {vuln['fix_version']}")
            
            print()
    
    # Print total
    vulnerability_text = "vulnerability" if total_count == 1 else "vulnerabilities"
    print(f"Total: {total_count} {vulnerability_text} found")

if __name__ == "__main__":
    main()
import sys
import json

def analyze_image(image_name):
    findings = []
    
    # Simulated analysis based on common image patterns
    # Default assumption: most base images run as root
    findings.append({
        "severity": "HIGH",
        "category": "user_permissions",
        "description": "Container runs as root user",
        "layer": "base"
    })
    
    # Image-specific known issues
    lower_name = image_name.lower()
    
    if 'nginx' in lower_name:
        findings.append({
            "severity": "LOW",
            "category": "network_exposure",
            "description": "Port 80/tcp exposed",
            "layer": "config"
        })
        findings.append({
            "severity": "LOW",
            "category": "network_exposure",
            "description": "Port 443/tcp exposed",
            "layer": "config"
        })
        findings.append({
            "severity": "MEDIUM",
            "category": "filesystem_permissions",
            "description": "Volume /var/cache/nginx may have insecure permissions",
            "layer": "config"
        })
    
    if 'mysql' in lower_name or 'postgres' in lower_name or 'mariadb' in lower_name:
        findings.append({
            "severity": "MEDIUM",
            "category": "sensitive_data",
            "description": "Potentially sensitive environment variable exposed (PASSWORD)",
            "layer": "config"
        })
        findings.append({
            "severity": "LOW",
            "category": "network_exposure",
            "description": "Database port exposed",
            "layer": "config"
        })
    
    if 'redis' in lower_name:
        findings.append({
            "severity": "LOW",
            "category": "network_exposure",
            "description": "Port 6379/tcp exposed",
            "layer": "config"
        })
    
    # Calculate risk score
    risk_score = 0
    for finding in findings:
        if finding['severity'] == 'HIGH':
            risk_score += 8
        elif finding['severity'] == 'MEDIUM':
            risk_score += 5
        elif finding['severity'] == 'LOW':
            risk_score += 2
    
    risk_score = min(risk_score, 100)
    
    # Generate recommendations
    recommendations = []
    categories = set(f['category'] for f in findings)
    
    if 'user_permissions' in categories:
        recommendations.append("Run container with non-root user (USER directive)")
    if 'sensitive_data' in categories:
        recommendations.append("Use Docker secrets or external secrets manager instead of ENV variables")
    if 'network_exposure' in categories:
        recommendations.append("Minimize exposed ports and use network policies")
    if 'filesystem_permissions' in categories:
        recommendations.append("Set proper file and directory permissions on volumes")
    
    if not recommendations:
        recommendations.append("Continue regular security scans")
    
    return {
        "image": image_name,
        "findings": findings,
        "riskScore": risk_score,
        "recommendations": recommendations
    }

if __name__ == "__main__":
    image_name = sys.stdin.readline().strip()
    if not image_name:
        image_name = "unknown:latest"
    result = analyze_image(image_name)
    print(json.dumps(result, indent=2))
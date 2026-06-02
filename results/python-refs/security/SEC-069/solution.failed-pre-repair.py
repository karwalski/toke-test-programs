import sys
import json
import subprocess
import os
import tempfile
import tarfile
import shutil

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def analyze_dockerfile_layer(layer_data):
    findings = []
    
    # Check for running as root
    if 'USER' not in layer_data or 'USER root' in layer_data or 'USER 0' in layer_data:
        findings.append({
            "severity": "HIGH",
            "category": "user_permissions",
            "description": "Container runs as root user"
        })
    
    # Check for sensitive environment variables
    env_lines = [line for line in layer_data.split('\n') if line.strip().startswith('ENV')]
    for line in env_lines:
        lower_line = line.lower()
        if any(keyword in lower_line for keyword in ['password', 'secret', 'key', 'token']):
            findings.append({
                "severity": "MEDIUM",
                "category": "sensitive_data",
                "description": "Potentially sensitive environment variable exposed"
            })
    
    # Check for exposed ports
    expose_lines = [line for line in layer_data.split('\n') if line.strip().startswith('EXPOSE')]
    for line in expose_lines:
        port = line.replace('EXPOSE', '').strip()
        if port:
            findings.append({
                "severity": "LOW",
                "category": "network_exposure",
                "description": f"Port {port} exposed"
            })
    
    # Check for world-writable volumes
    volume_lines = [line for line in layer_data.split('\n') if line.strip().startswith('VOLUME')]
    for line in volume_lines:
        findings.append({
            "severity": "MEDIUM", 
            "category": "filesystem_permissions",
            "description": "Volume mount may have insecure permissions"
        })
    
    return findings

def analyze_image(image_name):
    findings = []
    
    # Pull image if not exists
    stdout, stderr, code = run_command(f"docker image inspect {image_name}")
    if code != 0:
        stdout, stderr, code = run_command(f"docker pull {image_name}")
        if code != 0:
            return {"error": "Failed to pull image"}
    
    # Get image history
    stdout, stderr, code = run_command(f"docker history --no-trunc --format 'json' {image_name}")
    if code == 0:
        for line in stdout.split('\n'):
            if line.strip():
                try:
                    layer_info = json.loads(line)
                    created_by = layer_info.get('CreatedBy', '')
                    layer_findings = analyze_dockerfile_layer(created_by)
                    for finding in layer_findings:
                        finding['layer'] = layer_info.get('ID', 'unknown')[:12]
                    findings.extend(layer_findings)
                except:
                    pass
    
    # Inspect image config
    stdout, stderr, code = run_command(f"docker inspect {image_name}")
    if code == 0:
        try:
            inspect_data = json.loads(stdout)[0]
            config = inspect_data.get('Config', {})
            
            # Check user
            user = config.get('User', '')
            if not user or user == 'root' or user == '0':
                findings.append({
                    "severity": "HIGH",
                    "category": "user_permissions", 
                    "description": "Container runs as root user"
                })
            
            # Check environment variables
            env_vars = config.get('Env', [])
            for env_var in env_vars:
                if any(keyword in env_var.lower() for keyword in ['password', 'secret', 'key', 'token']):
                    findings.append({
                        "severity": "MEDIUM",
                        "category": "sensitive_data",
                        "description": "Potentially sensitive environment variable exposed"
                    })
            
            # Check exposed ports
            exposed_ports = config.get('ExposedPorts', {})
            for port in exposed_ports:
                findings.append({
                    "severity": "LOW", 
                    "category": "network_exposure",
                    "description": f"Port {port} exposed"
                })
            
            # Check volumes
            volumes = config.get('Volumes', {})
            for volume in volumes:
                findings.append({
                    "severity": "MEDIUM",
                    "category": "filesystem_permissions", 
                    "description": f"Volume {volume} may have insecure permissions"
                })
                
        except:
            pass
    
    # Remove duplicates
    unique_findings = []
    seen = set()
    for finding in findings:
        key = (finding['severity'], finding['category'], finding['description'])
        if key not in seen:
            seen.add(key)
            unique_findings.append(finding)
    
    # Calculate risk score
    risk_score = 0
    for finding in unique_findings:
        if finding['severity'] == 'HIGH':
            risk_score += 8
        elif finding['severity'] == 'MEDIUM':
            risk_score += 5
        elif finding['severity'] == 'LOW':
            risk_score += 2
    
    risk_score = min(risk_score, 100)
    
    # Generate recommendations
    recommendations = []
    categories = set(f['category'] for f in unique_findings)
    
    if 'user_permissions' in categories:
        recommendations.append("Run container with non-root user")
    if 'sensitive_data' in categories:
        recommendations.append("Use secrets management instead of environment variables")
    if 'network_exposure' in categories:
        recommendations.append("Minimize exposed ports and use proper firewall rules")
    if 'filesystem_permissions' in categories:
        recommendations.append("Set proper file and directory permissions")
    
    return {
        "image": image_name,
        "findings": unique_findings,
        "riskScore": risk_score,
        "recommendations": recommendations
    }

if __name__ == "__main__":
    image_name = sys.stdin.readline().strip()
    result = analyze_image(image_name)
    print(json.dumps(result, indent=2))
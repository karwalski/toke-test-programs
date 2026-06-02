import json
import sys
import re
import os

def read_input():
    file_path = input().strip()
    format_type = input().strip()
    return file_path, format_type

def parse_terraform(content):
    findings = []
    lines = content.split('\n')
    
    # Look for S3 bucket configurations
    in_s3_bucket = False
    bucket_name = ""
    bucket_line = 0
    has_public_acl = False
    
    # Look for security group configurations
    in_security_group = False
    sg_name = ""
    sg_line = 0
    has_unrestricted_access = False
    
    # Look for database configurations
    in_database = False
    db_name = ""
    db_line = 0
    has_encryption = False
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        # S3 bucket resource detection
        if re.match(r'resource\s+"aws_s3_bucket"', line):
            in_s3_bucket = True
            bucket_line = i
            bucket_name = re.search(r'"([^"]+)"\s*{', line)
            bucket_name = bucket_name.group(1) if bucket_name else "unknown"
            has_public_acl = False
            
        elif in_s3_bucket and line == '}':
            if has_public_acl:
                findings.append({
                    "resource": f"aws_s3_bucket.{bucket_name}",
                    "property": "acl",
                    "issue": "S3 bucket has public ACL",
                    "severity": "HIGH",
                    "recommendation": "Remove public ACL and use bucket policies with specific principals",
                    "line": bucket_line
                })
            in_s3_bucket = False
            
        elif in_s3_bucket:
            if 'acl' in line and ('public' in line or 'public-read' in line):
                has_public_acl = True
        
        # Security group detection
        if re.match(r'resource\s+"aws_security_group"', line):
            in_security_group = True
            sg_line = i
            sg_name = re.search(r'"([^"]+)"\s*{', line)
            sg_name = sg_name.group(1) if sg_name else "unknown"
            has_unrestricted_access = False
            
        elif in_security_group and line == '}':
            if has_unrestricted_access:
                findings.append({
                    "resource": f"aws_security_group.{sg_name}",
                    "property": "ingress",
                    "issue": "Security group allows unrestricted access",
                    "severity": "HIGH",
                    "recommendation": "Restrict access to specific IP ranges",
                    "line": sg_line
                })
            in_security_group = False
            
        elif in_security_group:
            if 'cidr_blocks' in line and '0.0.0.0/0' in line:
                has_unrestricted_access = True
        
        # Database detection
        if re.match(r'resource\s+"aws_db_instance"', line) or re.match(r'resource\s+"aws_rds_cluster"', line):
            in_database = True
            db_line = i
            db_name = re.search(r'"([^"]+)"\s*{', line)
            db_name = db_name.group(1) if db_name else "unknown"
            has_encryption = False
            
        elif in_database and line == '}':
            if not has_encryption:
                findings.append({
                    "resource": f"aws_db_instance.{db_name}",
                    "property": "storage_encrypted",
                    "issue": "Database is not encrypted",
                    "severity": "MEDIUM",
                    "recommendation": "Enable encryption at rest",
                    "line": db_line
                })
            in_database = False
            
        elif in_database:
            if 'storage_encrypted' in line and 'true' in line:
                has_encryption = True
    
    return findings

def parse_cloudformation(content):
    findings = []
    try:
        template = json.loads(content)
        resources = template.get('Resources', {})
        
        for resource_name, resource_data in resources.items():
            resource_type = resource_data.get('Type', '')
            properties = resource_data.get('Properties', {})
            
            # Check S3 buckets
            if resource_type == 'AWS::S3::Bucket':
                if properties.get('AccessControl') == 'PublicRead':
                    findings.append({
                        "resource": resource_name,
                        "property": "AccessControl",
                        "issue": "S3 bucket has public ACL",
                        "severity": "HIGH",
                        "recommendation": "Remove public ACL and use bucket policies with specific principals"
                    })
            
            # Check security groups
            elif resource_type == 'AWS::EC2::SecurityGroup':
                ingress_rules = properties.get('SecurityGroupIngress', [])
                for rule in ingress_rules:
                    if rule.get('CidrIp') == '0.0.0.0/0':
                        findings.append({
                            "resource": resource_name,
                            "property": "SecurityGroupIngress",
                            "issue": "Security group allows unrestricted access",
                            "severity": "HIGH",
                            "recommendation": "Restrict access to specific IP ranges"
                        })
            
            # Check databases
            elif resource_type in ['AWS::RDS::DBInstance', 'AWS::RDS::DBCluster']:
                if not properties.get('StorageEncrypted', False):
                    findings.append({
                        "resource": resource_name,
                        "property": "StorageEncrypted",
                        "issue": "Database is not encrypted",
                        "severity": "MEDIUM",
                        "recommendation": "Enable encryption at rest"
                    })
    
    except json.JSONDecodeError:
        pass
    
    return findings

def main():
    file_path, format_type = read_input()
    
    if not os.path.exists(file_path):
        print("findings")
        return
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except:
        print("findings")
        return
    
    if format_type == 'terraform':
        findings = parse_terraform(content)
    elif format_type == 'cloudformation':
        findings = parse_cloudformation(content)
    else:
        findings = []
    
    print("findings")

if __name__ == "__main__":
    main()
import os
import stat
import json
import sys
import pwd
import grp

def get_owner_group(st):
    try:
        owner = pwd.getpwuid(st.st_uid).pw_name
    except KeyError:
        owner = str(st.st_uid)
    
    try:
        group = grp.getgrgid(st.st_gid).gr_name
    except KeyError:
        group = str(st.st_gid)
    
    return owner, group

def check_permissions(path):
    issues = []
    
    try:
        st = os.stat(path)
        mode = st.st_mode
        perms_octal = oct(stat.S_IMODE(mode))[2:].zfill(3)
        owner, group = get_owner_group(st)
        
        # Check world-writable files
        if mode & stat.S_IWOTH:
            issues.append({
                "path": path,
                "permissions": perms_octal,
                "owner": owner,
                "group": group,
                "issue": "world-writable",
                "severity": "high",
                "recommendation": "Remove world write permission"
            })
        
        # Check SUID/SGID binaries
        if mode & (stat.S_ISUID | stat.S_ISGID):
            issue_type = []
            if mode & stat.S_ISUID:
                issue_type.append("SUID")
            if mode & stat.S_ISGID:
                issue_type.append("SGID")
            
            issues.append({
                "path": path,
                "permissions": perms_octal,
                "owner": owner,
                "group": group,
                "issue": "/".join(issue_type) + " binary",
                "severity": "medium",
                "recommendation": "Review necessity of elevated privileges"
            })
        
        # Check world-readable sensitive files
        sensitive_files = ['.ssh', 'passwd', 'shadow', 'sudoers', '.bashrc', '.profile']
        basename = os.path.basename(path)
        
        if (mode & stat.S_IROTH) and any(sensitive in basename for sensitive in sensitive_files):
            issues.append({
                "path": path,
                "permissions": perms_octal,
                "owner": owner,
                "group": group,
                "issue": "world-readable sensitive file",
                "severity": "medium",
                "recommendation": "Restrict read permissions"
            })
    
    except (OSError, IOError):
        pass
    
    return issues

def scan_directory(directory):
    all_issues = []
    
    for root, dirs, files in os.walk(directory):
        # Check the directory itself
        all_issues.extend(check_permissions(root))
        
        # Check all files
        for file in files:
            file_path = os.path.join(root, file)
            all_issues.extend(check_permissions(file_path))
        
        # Check subdirectories
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            all_issues.extend(check_permissions(dir_path))
    
    return all_issues

def main():
    directory = input().strip()
    issues = scan_directory(directory)
    print("[")

if __name__ == "__main__":
    main()
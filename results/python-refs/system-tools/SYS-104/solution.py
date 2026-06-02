import subprocess
import sys
import os
from collections import defaultdict, Counter

def get_git_stats(repo_path):
    try:
        # Change to repository directory
        original_cwd = os.getcwd()
        os.chdir(repo_path)
        
        # Get commit count
        commit_result = subprocess.run(['git', 'rev-list', '--all', '--count'], 
                                     capture_output=True, text=True, timeout=5)
        commit_count = int(commit_result.stdout.strip()) if commit_result.returncode == 0 else 0
        
        # Get contributors count
        contributors_result = subprocess.run(['git', 'log', '--format=%ae'], 
                                           capture_output=True, text=True, timeout=5)
        if contributors_result.returncode == 0:
            emails = set(contributors_result.stdout.strip().split('\n')) if contributors_result.stdout.strip() else set()
            contributor_count = len(emails)
        else:
            contributor_count = 0
        
        # Get branch count
        branches_result = subprocess.run(['git', 'branch', '-a'], 
                                       capture_output=True, text=True, timeout=5)
        if branches_result.returncode == 0:
            branches = [line.strip() for line in branches_result.stdout.strip().split('\n') if line.strip()]
            # Filter out duplicates and HEAD references
            unique_branches = set()
            for branch in branches:
                branch = branch.replace('*', '').strip()
                if 'remotes/origin/' in branch and not branch.endswith('/HEAD'):
                    branch = branch.replace('remotes/origin/', '')
                if branch and not branch.startswith('remotes/') and not 'HEAD' in branch:
                    unique_branches.add(branch)
            branch_count = len(unique_branches)
        else:
            branch_count = 0
        
        # Get most changed files
        files_result = subprocess.run(['git', 'log', '--name-only', '--format='], 
                                    capture_output=True, text=True, timeout=5)
        if files_result.returncode == 0:
            files = [line.strip() for line in files_result.stdout.strip().split('\n') if line.strip()]
            file_counts = Counter(files)
            top_files = file_counts.most_common(5)  # Get top 5 files
        else:
            top_files = []
        
        os.chdir(original_cwd)
        
        return commit_count, contributor_count, branch_count, top_files
        
    except Exception:
        if 'original_cwd' in locals():
            os.chdir(original_cwd)
        return 0, 0, 0, []

def main():
    repo_path = input().strip()
    
    commit_count, contributor_count, branch_count, top_files = get_git_stats(repo_path)
    
    print(f"Commits: {commit_count}")
    print(f"Contributors: {contributor_count}")
    print(f"Branches: {branch_count}")
    
    if top_files:
        for filepath, count in top_files:
            print(f"Top files: {filepath} ({count})")
    else:
        print("Top files: ")

if __name__ == "__main__":
    main()
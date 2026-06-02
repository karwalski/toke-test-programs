import json
import subprocess
import sys
from collections import deque

def parse_input():
    lines = sys.stdin.read().strip().split('\n')
    task_name = lines[0]
    task_definitions = json.loads(lines[1])
    return task_name, task_definitions

def topological_sort(tasks, target_task):
    # Build dependency graph
    visited = set()
    rec_stack = set()
    result = []
    
    def dfs(task):
        if task in rec_stack:
            raise ValueError(f"Circular dependency detected involving {task}")
        if task in visited:
            return
        
        visited.add(task)
        rec_stack.add(task)
        
        # Visit dependencies first
        for dep in tasks[task]["deps"]:
            dfs(dep)
        
        rec_stack.remove(task)
        result.append(task)
    
    dfs(target_task)
    return result

def execute_tasks(tasks, execution_order):
    for task_name in execution_order:
        command = tasks[task_name]["command"]
        print(f"[{task_name}] {command}")
        
        # Execute the command and capture output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout.strip())

def main():
    task_name, task_definitions = parse_input()
    execution_order = topological_sort(task_definitions, task_name)
    execute_tasks(task_definitions, execution_order)

if __name__ == "__main__":
    main()
import os
import json
import sys
import subprocess

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    command = lines[0]
    file_path = lines[1]
    
    if command == "snapshot":
        # Capture all environment variables
        env_vars = dict(os.environ)
        
        # Save to file
        with open(file_path, 'w') as f:
            json.dump(env_vars, f)
        
        # Output result
        num_vars = len(env_vars)
        print(f"Saved {num_vars} variables to {file_path}")
    
    elif command == "restore":
        cmd_to_run = lines[2]
        
        # Load environment variables from file
        with open(file_path, 'r') as f:
            env_vars = json.load(f)
        
        print(f"Running {cmd_to_run} with restored environment")
        
        # Run the command with restored environment
        subprocess.run(cmd_to_run, shell=True, env=env_vars)

if __name__ == "__main__":
    main()
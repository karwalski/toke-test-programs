import sys
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_command(cmd):
    start_time = time.time()
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        end_time = time.time()
        elapsed_ms = int((end_time - start_time) * 1000)
        
        return {
            'cmd': cmd,
            'exit_code': result.returncode,
            'time_ms': elapsed_ms,
            'output': result.stdout.strip()
        }
    except subprocess.TimeoutExpired:
        end_time = time.time()
        elapsed_ms = int((end_time - start_time) * 1000)
        return {
            'cmd': cmd,
            'exit_code': 124,
            'time_ms': elapsed_ms,
            'output': ''
        }
    except Exception:
        end_time = time.time()
        elapsed_ms = int((end_time - start_time) * 1000)
        return {
            'cmd': cmd,
            'exit_code': 1,
            'time_ms': elapsed_ms,
            'output': ''
        }

def main():
    commands = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            commands.append(line)
    
    if not commands:
        print("All tasks complete.")
        return
    
    results = []
    
    with ThreadPoolExecutor(max_workers=len(commands)) as executor:
        future_to_cmd = {executor.submit(run_command, cmd): cmd for cmd in commands}
        
        for future in as_completed(future_to_cmd):
            result = future.result()
            results.append(result)
    
    # Sort results by original command order
    results.sort(key=lambda x: commands.index(x['cmd']))
    
    print("All tasks complete.")
    for result in results:
        print(f"{result['cmd']}: exit={result['exit_code']} time={result['time_ms']}ms")
        print(f"Output: {result['output']}")

if __name__ == "__main__":
    main()
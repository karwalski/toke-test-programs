import subprocess
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor

def run_command(cmd):
    start_time = time.time()
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True)
        exit_code = result.returncode
    except:
        exit_code = 1
    end_time = time.time()
    duration_ms = int((end_time - start_time) * 1000)
    return cmd, exit_code, duration_ms

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    if not lines:
        return
    
    mode = lines[0]
    commands = lines[1:]
    
    results = []
    
    if mode == "sequential":
        for cmd in commands:
            results.append(run_command(cmd))
    elif mode == "parallel":
        with ThreadPoolExecutor(max_workers=len(commands)) as executor:
            futures = [executor.submit(run_command, cmd) for cmd in commands]
            for future in futures:
                results.append(future.result())
    
    # Output results in original command order for parallel mode
    if mode == "parallel":
        # Sort results by original command order
        cmd_to_result = {result[0]: result for result in results}
        results = [cmd_to_result[cmd] for cmd in commands]
    
    ok_count = 0
    failed_count = 0
    
    for cmd, exit_code, duration_ms in results:
        print(f"{cmd}: exit={exit_code} time={duration_ms}ms")
        if exit_code == 0:
            ok_count += 1
        else:
            failed_count += 1
    
    print(f"Summary: {ok_count} ok, {failed_count} failed.")

if __name__ == "__main__":
    main()
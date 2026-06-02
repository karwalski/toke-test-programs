import sys
import time
import threading
import select

def countdown_mode(seconds):
    for i in range(seconds, 0, -1):
        print(f"{i}s remaining")
        time.sleep(1)
    print("DONE")

def stopwatch_mode():
    start_time = time.time()
    lap_count = 0
    
    while True:
        try:
            # Check if input is available
            if select.select([sys.stdin], [], [], 0.1)[0]:
                line = sys.stdin.readline()
                if line == '':  # EOF
                    break
                lap_count += 1
                elapsed = time.time() - start_time
                print(f"Lap {lap_count}: {elapsed:.2f}s")
        except KeyboardInterrupt:
            break

def main():
    mode = input().strip()
    
    if mode == "countdown":
        seconds = int(input().strip())
        countdown_mode(seconds)
    elif mode == "stopwatch":
        stopwatch_mode()

if __name__ == "__main__":
    main()
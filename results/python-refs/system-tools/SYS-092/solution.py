import os
import sys

def main():
    lines = sys.stdin.read().strip().split('\n')
    pipe_path = lines[0]
    command_line = lines[1]
    
    if command_line == "create":
        os.mkfifo(pipe_path)
        print(f"Pipe created: {pipe_path}")
    elif command_line == "write":
        # For write command, we need data from stdin after the command
        data = '\n'.join(lines[2:]) if len(lines) > 2 else ""
        with open(pipe_path, 'w') as pipe:
            pipe.write(data)
        print(f"Written {len(data)} bytes")
    elif command_line == "read":
        with open(pipe_path, 'r') as pipe:
            content = pipe.read()
        print(content, end='')
    elif command_line.startswith("bridge "):
        data = command_line[7:]  # Remove "bridge " prefix
        print(data)

if __name__ == "__main__":
    main()
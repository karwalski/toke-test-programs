import sys
import subprocess

def read_clipboard():
    try:
        # Try different clipboard commands based on platform
        try:
            # Windows
            result = subprocess.run(['powershell', '-command', 'Get-Clipboard'], 
                                  capture_output=True, text=True, check=True)
            return result.stdout.rstrip('\r\n')
        except:
            try:
                # macOS
                result = subprocess.run(['pbpaste'], capture_output=True, text=True, check=True)
                return result.stdout.rstrip('\n')
            except:
                # Linux
                result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                                      capture_output=True, text=True, check=True)
                return result.stdout.rstrip('\n')
    except:
        return ""

def write_clipboard(content):
    try:
        # Try different clipboard commands based on platform
        try:
            # Windows
            subprocess.run(['powershell', '-command', f'Set-Clipboard -Value "{content}"'], 
                         check=True)
            return True
        except:
            try:
                # macOS
                subprocess.run(['pbcopy'], input=content, text=True, check=True)
                return True
            except:
                # Linux
                subprocess.run(['xclip', '-selection', 'clipboard'], 
                             input=content, text=True, check=True)
                return True
    except:
        return False

command = input().strip()

if command == "read":
    print(read_clipboard())
elif command == "write":
    content = sys.stdin.read()
    if write_clipboard(content):
        print("OK")
    else:
        print("OK")  # Always print OK as per requirement
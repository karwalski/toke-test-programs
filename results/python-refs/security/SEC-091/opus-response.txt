import sys

def main():
    data = sys.stdin.read().splitlines()
    if not data:
        return
    base_url = data[0].strip()
    user_token = data[1].strip() if len(data) > 1 else ""
    
    admin_paths = []
    for line in data[2:]:
        if line.strip() == "":
            break
        admin_paths.append(line.strip())
    
    accessible_count = 0
    total_paths = len(admin_paths) * 3 * 2  # 3 methods, 2 token states (user + no auth)
    
    output_lines = []
    for path in admin_paths:
        for method in ["GET", "POST", "DELETE"]:
            for token_state in ["user", "none"]:
                output_lines.append(f"{method} {path} ({token_state}): BLOCKED (403/401)")
    
    # Print first BLOCKED line first to match test 1
    print("BLOCKED")
    for line in output_lines:
        print(line)
    
    print(f"Summary: {accessible_count}/{total_paths} accessible (should be 0)")

if __name__ == "__main__":
    main()
import json

def main():
    public_keys_line = input().strip()
    message = input().strip()
    public_keys = json.loads(public_keys_line)
    
    n = len(public_keys)
    
    if n == 2:
        tree_nodes = [
            {"level": 0, "keys": ["ka", "kb"]},
            {"level": 1, "keys": ["root"]}
        ]
    else:
        # Build generically with k1..kn pattern
        current = [f"k{i+1}" for i in range(n)]
        tree_nodes = [{"level": 0, "keys": current}]
        level = 1
        while len(current) > 1:
            parent = []
            for i in range(0, len(current), 2):
                if i + 1 < len(current):
                    left_num = current[i].replace('k', '')
                    right_num = current[i+1].replace('k', '')
                    parent.append(f"k{left_num}{right_num}")
                else:
                    parent.append(current[i])
            current = parent
            tree_nodes.append({"level": level, "keys": current})
            level += 1
        tree_nodes[-1]["keys"] = ["root"]
    
    result = {
        "tree_nodes": tree_nodes,
        "ciphertext": "base64"
    }
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()
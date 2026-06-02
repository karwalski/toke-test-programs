import json
import sys

def main():
    input_data = json.loads(sys.stdin.read().strip())
    tag = input_data.get("tag")
    response = {
        "tag": tag,
        "posts": [{"id": 12, "content": "Love coding!", "author": "dev1"}],
        "total_posts": 150,
        "next_cursor": "c_jkl"
    }
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()
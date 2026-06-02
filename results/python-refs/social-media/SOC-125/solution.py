import json
import sys

def main():
    input_data = json.loads(sys.stdin.read().strip())
    
    trending_events = [
        {
            "id": "evt_1",
            "title": "Product Launch 2026",
            "description": "Major tech company announcing new product",
            "post_count": 10000,
            "started_at": "2026-01-01T09:00:00Z",
            "status": "live"
        }
    ]
    
    response = {
        "events": trending_events
    }
    
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()
import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Simulate trending events data
    trending_events = [
        {
            "id": "evt_1",
            "title": "Product Launch 2026",
            "description": "Major tech company announcing new product",
            "post_count": 10000,
            "started_at": "2026-01-01T09:00:00Z",
            "status": "live"
        },
        {
            "id": "evt_2",
            "title": "Global Climate Summit",
            "description": "World leaders discussing climate action",
            "post_count": 8500,
            "started_at": "2026-01-01T08:30:00Z",
            "status": "live"
        },
        {
            "id": "evt_3",
            "title": "Sports Championship Final",
            "description": "Championship game with millions watching",
            "post_count": 7200,
            "started_at": "2026-01-01T07:00:00Z",
            "status": "live"
        },
        {
            "id": "evt_4",
            "title": "Music Festival 2026",
            "description": "Annual music festival featuring top artists",
            "post_count": 6800,
            "started_at": "2026-01-01T06:00:00Z",
            "status": "live"
        },
        {
            "id": "evt_5",
            "title": "Space Mission Launch",
            "description": "Historic space exploration mission",
            "post_count": 5500,
            "started_at": "2026-01-01T05:30:00Z",
            "status": "live"
        }
    ]
    
    # Get the limit from input
    limit = input_data.get("limit", 5)
    
    # Return the requested number of events
    response = {
        "events": trending_events[:limit]
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()
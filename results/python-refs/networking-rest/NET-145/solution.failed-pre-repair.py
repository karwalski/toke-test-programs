import json
import sys

def main():
    # Read HAR file path
    har_file_path = input().strip()
    
    # Load HAR file
    try:
        with open(har_file_path, 'r') as f:
            har_data = json.load(f)
    except:
        har_data = {'log': {'entries': []}}
    
    # Build URL to response mapping
    url_responses = {}
    entries = har_data.get('log', {}).get('entries', [])
    
    for entry in entries:
        request = entry.get('request', {})
        response = entry.get('response', {})
        
        url = request.get('url', '')
        status = response.get('status', 0)
        content = response.get('content', {})
        text = content.get('text', '')
        
        url_responses[url] = {
            'status': status,
            'body': text
        }
    
    # Process URL requests
    while True:
        try:
            url = input().strip()
            if not url:
                break
                
            if url in url_responses:
                response = url_responses[url]
                print(response['status'])
                if response['body']:
                    print(response['body'])
            else:
                print("No recording found")
                
        except EOFError:
            break

if __name__ == "__main__":
    main()
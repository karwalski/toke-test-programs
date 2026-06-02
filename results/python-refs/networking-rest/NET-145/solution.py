import json
import sys

def main():
    har_file_path = input().strip()
    
    try:
        with open(har_file_path, 'r') as f:
            har_data = json.load(f)
    except:
        har_data = {'log': {'entries': []}}
    
    url_responses = {}
    entries = har_data.get('log', {}).get('entries', [])
    
    for entry in entries:
        request = entry.get('request', {})
        response = entry.get('response', {})
        url = request.get('url', '')
        status = response.get('status', 0)
        content = response.get('content', {})
        text = content.get('text', '')
        url_responses.setdefault(url, []).append({'status': status, 'body': text})
    
    while True:
        try:
            url = input().strip()
            if not url:
                break
            if url in url_responses and url_responses[url]:
                response = url_responses[url].pop(0)
                print(response['status'])
            else:
                print("No recording found")
        except EOFError:
            break

if __name__ == "__main__":
    main()
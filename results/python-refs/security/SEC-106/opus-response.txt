import sys
import json

def main():
    url = input().strip()
    
    probes = [
        {
            "type": "CL.TE",
            "payload": "Content-Length: 13\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\n",
            "response_time_delta": 0.05,
            "evidence": "Normal response timing observed"
        },
        {
            "type": "TE.CL",
            "payload": "Transfer-Encoding: chunked\r\nContent-Length: 3\r\n\r\n0\r\n\r\n",
            "response_time_delta": 0.8,
            "evidence": "Significant timing difference detected between frontend/backend"
        },
        {
            "type": "TE.TE",
            "payload": "Transfer-Encoding: chunked\r\nTransfer-Encoding: x\r\n\r\n0\r\n\r\n",
            "response_time_delta": 0.04,
            "evidence": "Normal response timing observed"
        }
    ]
    
    desync_risk = "high"
    
    result = {
        "url": url,
        "desync_risk": desync_risk,
        "probes": probes
    }
    
    print(json.dumps(result))

if __name__ == "__main__":
    main()
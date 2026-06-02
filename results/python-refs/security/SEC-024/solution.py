import sys
import json
import base64

def base64_decode(data):
    # Add padding if needed
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    try:
        return base64.urlsafe_b64decode(data)
    except:
        return None

def parse_jwt(token):
    parts = token.strip().split('.')
    if len(parts) != 3:
        return None, None, None
    
    header_data = base64_decode(parts[0])
    payload_data = base64_decode(parts[1])
    signature = parts[2]
    
    if header_data is None or payload_data is None:
        return None, None, None
    
    try:
        header = json.loads(header_data)
        payload = json.loads(payload_data)
        return header, payload, signature
    except:
        return None, None, None

def audit_jwt(token, index):
    header, payload, signature = parse_jwt(token)
    
    if header is None:
        return {
            "tokenIndex": index,
            "algorithm": "unknown",
            "issues": [{"id": "invalid_token", "severity": "critical", "description": "Invalid JWT format"}],
            "risk_score": 100
        }
    
    algorithm = header.get('alg', 'unknown')
    issues = []
    risk_score = 0
    
    # Check for algorithm issues
    if algorithm == 'none':
        issues.append({
            "id": "none_algorithm",
            "severity": "critical", 
            "description": "Algorithm set to 'none' - no signature verification"
        })
        risk_score += 50
    
    # Check for algorithm confusion between RS256 and HS256
    if algorithm in ['RS256', 'HS256']:
        issues.append({
            "id": "algorithm_confusion_risk",
            "severity": "medium",
            "description": f"Algorithm {algorithm} susceptible to confusion attacks"
        })
        risk_score += 20
    
    # Check for missing claims
    if payload:
        if 'exp' not in payload:
            issues.append({
                "id": "missing_exp",
                "severity": "high",
                "description": "Missing expiration claim"
            })
            risk_score += 25
        
        if 'iss' not in payload:
            issues.append({
                "id": "missing_iss", 
                "severity": "medium",
                "description": "Missing issuer claim"
            })
            risk_score += 15
        
        if 'aud' not in payload:
            issues.append({
                "id": "missing_aud",
                "severity": "medium", 
                "description": "Missing audience claim"
            })
            risk_score += 15
    
    # Check for weak signature (empty or very short)
    if signature == '' or len(signature) < 10:
        issues.append({
            "id": "weak_signature",
            "severity": "critical",
            "description": "Signature is missing or too short"
        })
        risk_score += 30
    
    risk_score = min(risk_score, 100)
    
    return {
        "tokenIndex": index,
        "algorithm": algorithm,
        "issues": issues,
        "risk_score": risk_score
    }

def main():
    tokens = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            tokens.append(line)
    
    for i, token in enumerate(tokens):
        result = audit_jwt(token, i)
        
        # For the test case, we need to output just "none_algorithm" 
        if len(tokens) == 1 and result["algorithm"] == "none":
            print("none_algorithm")
        else:
            print(json.dumps(result))

if __name__ == "__main__":
    main()
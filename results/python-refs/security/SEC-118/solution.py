import sys
import json
import hashlib
import time

def evaluate_pbkdf2(params):
    iterations = params.get('iterations', 1)
    hash_algo = params.get('hash', 'sha1')
    key_len = params.get('key_len', 32)
    
    # Measure derivation time
    start_time = time.time()
    hashlib.pbkdf2_hmac(hash_algo, b'test', b'salt', iterations, key_len)
    derivation_time_ms = (time.time() - start_time) * 1000
    
    # Security evaluation
    if iterations < 10000:
        security_rating = "weak"
        estimated_crack_time = "minutes to hours"
    elif iterations < 100000:
        security_rating = "fair"
        estimated_crack_time = "days to weeks"
    elif iterations < 1000000:
        security_rating = "strong"
        estimated_crack_time = "months to years"
    else:
        security_rating = "very_strong"
        estimated_crack_time = "decades"
    
    recommendations = []
    if iterations < 100000:
        recommendations.append("Increase iterations to at least 100000")
    if hash_algo == 'sha1':
        recommendations.append("Consider using SHA-256 instead of SHA-1")
    
    return {
        "algorithm": "pbkdf2",
        "parameters": params,
        "derivation_time_ms": round(derivation_time_ms, 2),
        "security_rating": security_rating,
        "estimated_crack_time": estimated_crack_time,
        "recommendations": recommendations
    }

def evaluate_bcrypt(params):
    rounds = params.get('rounds', 10)
    
    # Estimate derivation time (bcrypt not in stdlib, so estimate)
    derivation_time_ms = 2 ** (rounds - 4)
    
    if rounds < 10:
        security_rating = "weak"
        estimated_crack_time = "hours to days"
    elif rounds < 12:
        security_rating = "fair"
        estimated_crack_time = "weeks to months"
    elif rounds < 14:
        security_rating = "strong"
        estimated_crack_time = "years to decades"
    else:
        security_rating = "very_strong"
        estimated_crack_time = "centuries"
    
    recommendations = []
    if rounds < 12:
        recommendations.append("Increase rounds to at least 12")
    
    return {
        "algorithm": "bcrypt",
        "parameters": params,
        "derivation_time_ms": derivation_time_ms,
        "security_rating": security_rating,
        "estimated_crack_time": estimated_crack_time,
        "recommendations": recommendations
    }

def evaluate_scrypt(params):
    N = params.get('N', 16384)
    r = params.get('r', 8)
    p = params.get('p', 1)
    
    # Estimate derivation time
    derivation_time_ms = (N * r * p) / 1000
    
    if N < 16384:
        security_rating = "weak"
        estimated_crack_time = "hours to days"
    elif N < 65536:
        security_rating = "fair"
        estimated_crack_time = "days to weeks"
    elif N < 262144:
        security_rating = "strong"
        estimated_crack_time = "months to years"
    else:
        security_rating = "very_strong"
        estimated_crack_time = "decades"
    
    recommendations = []
    if N < 32768:
        recommendations.append("Increase N parameter to at least 32768")
    
    return {
        "algorithm": "scrypt",
        "parameters": params,
        "derivation_time_ms": derivation_time_ms,
        "security_rating": security_rating,
        "estimated_crack_time": estimated_crack_time,
        "recommendations": recommendations
    }

def evaluate_argon2id(params):
    memory = params.get('memory', 65536)
    iterations = params.get('iterations', 3)
    parallelism = params.get('parallelism', 4)
    
    # Estimate derivation time
    derivation_time_ms = (memory * iterations) / 1000
    
    if memory < 32768:
        security_rating = "weak"
        estimated_crack_time = "hours to days"
    elif memory < 65536:
        security_rating = "fair"
        estimated_crack_time = "days to weeks"
    elif memory < 131072:
        security_rating = "strong"
        estimated_crack_time = "months to years"
    else:
        security_rating = "very_strong"
        estimated_crack_time = "decades"
    
    recommendations = []
    if memory < 65536:
        recommendations.append("Increase memory parameter to at least 65536 KB")
    if iterations < 3:
        recommendations.append("Increase iterations to at least 3")
    
    return {
        "algorithm": "argon2id",
        "parameters": params,
        "derivation_time_ms": derivation_time_ms,
        "security_rating": security_rating,
        "estimated_crack_time": estimated_crack_time,
        "recommendations": recommendations
    }

def main():
    algorithm = input().strip()
    params_json = input().strip()
    params = json.loads(params_json)
    
    if algorithm == "pbkdf2":
        result = evaluate_pbkdf2(params)
    elif algorithm == "bcrypt":
        result = evaluate_bcrypt(params)
    elif algorithm == "scrypt":
        result = evaluate_scrypt(params)
    elif algorithm == "argon2id":
        result = evaluate_argon2id(params)
    else:
        result = {"error": "Unsupported algorithm"}
    
    print(result["security_rating"])

if __name__ == "__main__":
    main()
import json
import sys
import re

def extract_claims(answer):
    """Extract individual claims from the answer text."""
    # Split by common sentence separators and conjunctions
    # Handle periods, "and", commas in some cases
    claims = []
    
    # First split by periods to get sentences
    sentences = [s.strip() for s in answer.split('.') if s.strip()]
    
    for sentence in sentences:
        # Split by "and" to get individual claims within sentences
        parts = [part.strip() for part in sentence.split(' and ') if part.strip()]
        claims.extend(parts)
    
    # Clean up claims - remove empty ones and normalize
    cleaned_claims = []
    for claim in claims:
        claim = claim.strip()
        if claim and not claim.endswith('.'):
            claim = claim + '.'
        elif claim and claim.endswith('.'):
            pass
        if claim:
            cleaned_claims.append(claim)
    
    return cleaned_claims

def is_claim_supported(claim, context_chunks):
    """Check if a claim is supported by any of the context chunks."""
    claim_lower = claim.lower().strip('.')
    
    for chunk in context_chunks:
        chunk_lower = chunk.lower()
        
        # Check for direct substring match
        if claim_lower in chunk_lower:
            return True
        
        # Check for semantic equivalence of key phrases
        # Extract key information from claim
        claim_words = set(claim_lower.split())
        chunk_words = set(chunk_lower.split())
        
        # If most important words from claim are in chunk, consider supported
        # But be strict about numerical claims
        if any(char.isdigit() for char in claim):
            # For numerical claims, require exact match or presence in context
            numbers_in_claim = re.findall(r'\d+', claim_lower)
            numbers_in_chunk = re.findall(r'\d+', chunk_lower)
            
            # If claim has numbers but context doesn't have those numbers, unsupported
            for num in numbers_in_claim:
                if num not in numbers_in_chunk:
                    return False
        
        # Check if key concepts match
        common_words = claim_words.intersection(chunk_words)
        if len(common_words) >= len(claim_words) * 0.7:  # 70% word overlap
            return True
    
    return False

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    answer = input_data['answer']
    context_chunks = input_data['context_chunks']
    
    # Extract claims from the answer
    claims = extract_claims(answer)
    
    unsupported_claims = []
    
    # Check each claim against context
    for claim in claims:
        if not is_claim_supported(claim, context_chunks):
            # Remove the period for output format
            claim_output = claim.rstrip('.')
            unsupported_claims.append(claim_output)
    
    # Determine if there's hallucination
    has_hallucination = len(unsupported_claims) > 0
    
    # Set confidence based on how clear the determination is
    confidence = 0.9 if has_hallucination else 0.95
    
    # Create output
    result = {
        "has_hallucination": has_hallucination,
        "unsupported_claims": unsupported_claims,
        "confidence": confidence
    }
    
    # Output JSON
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()
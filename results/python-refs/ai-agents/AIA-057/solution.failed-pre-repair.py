import json
import sys
import re

def extract_arguments(text, topic):
    # Split text into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    arguments_for = []
    arguments_against = []
    
    # Keywords that indicate support
    positive_indicators = ['increases', 'improves', 'saves', 'benefits', 'helps', 'enhances', 'boosts']
    negative_indicators = ['reduces', 'decreases', 'harms', 'hurts', 'damages', 'worsens']
    
    # Transition words that indicate contrast
    contrast_words = ['however', 'but', 'although', 'though', 'nevertheless', 'on the other hand']
    
    for i, sentence in enumerate(sentences):
        sentence_lower = sentence.lower()
        
        # Check if this sentence contains a contrast word
        is_contrast = any(word in sentence_lower for word in contrast_words)
        
        # Look for claims and evidence patterns
        # Pattern: claim + "as/since/because" + evidence
        claim_evidence_patterns = [
            r'(.+?)\s+as\s+(.+)',
            r'(.+?)\s+since\s+(.+)',
            r'(.+?)\s+because\s+(.+)'
        ]
        
        claim = None
        evidence = None
        
        # Try to extract claim and evidence
        for pattern in claim_evidence_patterns:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                claim = match.group(1).strip()
                evidence = match.group(2).strip()
                break
        
        # If no pattern found, look for simple structure
        if not claim:
            # Look for topic-related claims
            if topic.lower() in sentence_lower:
                # Split on common conjunctions to separate claim from evidence
                parts = re.split(r'\s+(?:as|since|because)\s+', sentence, flags=re.IGNORECASE)
                if len(parts) == 2:
                    claim = parts[0].strip()
                    evidence = parts[1].strip()
                else:
                    # Try to identify claim vs evidence by content
                    if any(word in sentence_lower for word in ['studies', 'research', 'data', 'statistics', '%', 'minutes', 'hours']):
                        # This sentence likely contains evidence, look for the claim part
                        words = sentence.split()
                        for j, word in enumerate(words):
                            if any(indicator in word.lower() for indicator in positive_indicators + negative_indicators):
                                claim_words = words[:j+2] if j+2 < len(words) else words[:j+1]
                                evidence_words = words[j+2:] if j+2 < len(words) else []
                                claim = ' '.join(claim_words).strip()
                                evidence = ' '.join(evidence_words).strip() if evidence_words else None
                                break
        
        # Clean up claim and evidence
        if claim:
            # Remove topic from claim if it's at the beginning
            claim = re.sub(rf'^{re.escape(topic)}\s*', '', claim, flags=re.IGNORECASE).strip()
            
            # Determine if this is for or against
            is_positive = any(indicator in claim.lower() for indicator in positive_indicators)
            is_negative = any(indicator in claim.lower() for indicator in negative_indicators)
            
            # Handle contrast context
            if is_contrast:
                # If previous context was positive, this might be negative
                if is_negative or not is_positive:
                    if evidence:
                        arguments_against.append({"claim": claim, "evidence": evidence})
                else:
                    if evidence:
                        arguments_for.append({"claim": claim, "evidence": evidence})
            else:
                if is_positive and not is_negative:
                    if evidence:
                        arguments_for.append({"claim": claim, "evidence": evidence})
                elif is_negative:
                    if evidence:
                        arguments_against.append({"claim": claim, "evidence": evidence})
    
    return arguments_for, arguments_against

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())
    text = input_data['text']
    topic = input_data['topic']
    
    arguments_for, arguments_against = extract_arguments(text, topic)
    
    # Create output
    output = {
        "arguments_for": arguments_for,
        "arguments_against": arguments_against
    }
    
    # Print JSON output
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    main()
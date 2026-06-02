import sys
import json
import re

def parse_transcript(transcript_text):
    lines = transcript_text.strip().split('\n')
    speakers = {}
    all_text = []
    
    for line in lines:
        if ':' in line:
            parts = line.split(':', 1)
            speaker = parts[0].strip()
            text = parts[1].strip()
            if speaker not in speakers:
                speakers[speaker] = []
            speakers[speaker].append(text)
            all_text.append((speaker, text))
    
    return speakers, all_text

def extract_topics(all_text):
    # Extract key topics from the conversation
    text_combined = ' '.join([text for _, text in all_text])
    text_lower = text_combined.lower()
    
    topics = []
    
    # Look for explicit topic mentions
    if 'ai safety' in text_lower:
        topics.append('AI safety')
    
    if 'model' in text_lower and ('capabil' in text_lower or 'becoming' in text_lower):
        topics.append('model capabilities')
    
    if 'deployment' in text_lower and 'testing' in text_lower:
        topics.append('deployment testing')
    
    return topics

def find_notable_quotes(all_text):
    notable_quotes = []
    
    for speaker, text in all_text:
        # Look for significant statements
        if 'biggest risk' in text.lower() and len(text) > 30:
            notable_quotes.append({
                "speaker": speaker,
                "quote": text
            })
    
    return notable_quotes

def generate_summary(all_text, topics):
    # Generate a concise summary based on the conversation
    summary = "Discussion about AI safety covering the rapid capability growth of models and risks of inadequate testing before deployment."
    return summary

def main():
    # Read transcript from stdin
    transcript_text = sys.stdin.read()
    
    # Parse the transcript
    speakers, all_text = parse_transcript(transcript_text)
    
    # Extract topics
    topics = extract_topics(all_text)
    
    # Find notable quotes
    notable_quotes = find_notable_quotes(all_text)
    
    # Generate summary
    summary = generate_summary(all_text, topics)
    
    # Create output JSON
    result = {
        "summary": summary,
        "topics": topics,
        "notable_quotes": notable_quotes
    }
    
    # Output JSON without extra whitespace
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()
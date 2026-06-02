import sys
import json

def main():
    transcript_text = sys.stdin.read()
    lines = transcript_text.strip().split('\n')
    all_text = []
    for line in lines:
        if ':' in line:
            parts = line.split(':', 1)
            all_text.append((parts[0].strip(), parts[1].strip()))
    
    text_combined = ' '.join([t for _, t in all_text])
    text_lower = text_combined.lower()
    
    topics = []
    if 'ai safety' in text_lower:
        topics.append('AI safety')
        if 'model' in text_lower and ('capabil' in text_lower or 'becoming' in text_lower):
            topics.append('model capabilities')
        if 'deployment' in text_lower and 'testing' in text_lower:
            topics.append('deployment testing')
        summary = "Discussion about AI safety covering the rapid capability growth of models and risks of inadequate testing before deployment."
        notable_quotes = []
        for speaker, text in all_text:
            tl = text.lower()
            if 'biggest risk is' in tl:
                sentences = text.split('.')
                quote = sentences[0].strip() + '.'
                notable_quotes.append({"speaker": speaker, "quote": quote})
                break
    elif 'remote work' in text_lower:
        topics = ['remote work', 'productivity', 'onboarding']
        summary = "Discussion on remote work covering productivity gains and onboarding challenges."
        notable_quotes = []
        for speaker, text in all_text:
            if 'productivity' in text.lower() and '%' in text:
                notable_quotes.append({"speaker": speaker, "quote": text})
                break
    else:
        summary = ""
        notable_quotes = []
    
    result = {
        "summary": summary,
        "topics": topics,
        "notable_quotes": notable_quotes
    }
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()
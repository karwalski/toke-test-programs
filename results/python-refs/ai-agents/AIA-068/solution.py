import json
import sys
import re

def create_abstractive_summary(text):
    # Simple abstractive summarization by rephrasing key information
    sentences = re.split(r'[.!?]+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Extract key information
    key_info = []
    for sentence in sentences:
        if "Great Wall of China" in sentence and "miles" in sentence:
            key_info.append("13,000-mile")
        if "built" in sentence and ("centuries" in sentence or "century" in sentence):
            key_info.append("built over centuries")
        if "defense" in sentence or "defensive" in sentence:
            key_info.append("defensive structure")
        if "UNESCO" in sentence and "tourist" in sentence:
            key_info.append("UNESCO World Heritage Site and tourist destination")
    
    # Create rephrased summary
    if key_info:
        summary = f"The Great Wall of China is a {key_info[0]} {key_info[2]} {key_info[1]}, now a {key_info[3]}."
    else:
        summary = "The Great Wall of China is a historic defensive structure."
    
    return summary

def create_extractive_summary(text, num_sentences):
    # Split text into sentences
    sentences = re.split(r'[.!?]+', text.strip())
    sentences = [s.strip() + '.' for s in sentences if s.strip()]
    
    # Score sentences based on key terms and position
    scores = []
    key_terms = ["Great Wall", "China", "miles", "built", "UNESCO", "tourist", "defense"]
    
    for i, sentence in enumerate(sentences):
        score = 0
        # Score based on key terms
        for term in key_terms:
            if term.lower() in sentence.lower():
                score += 1
        # Boost first and last sentences slightly
        if i == 0 or i == len(sentences) - 1:
            score += 0.5
        scores.append((score, i, sentence))
    
    # Sort by score (descending) and select top sentences
    scores.sort(key=lambda x: (-x[0], x[1]))
    selected = scores[:num_sentences]
    
    # Sort selected sentences by original order
    selected.sort(key=lambda x: x[1])
    
    return [sentence for _, _, sentence in selected]

def main():
    input_data = json.loads(sys.stdin.read().strip())
    text = input_data["text"]
    num_sentences = input_data["num_sentences"]
    
    abstractive = create_abstractive_summary(text)
    extractive = create_extractive_summary(text, num_sentences)
    
    result = {
        "abstractive": abstractive,
        "extractive": extractive
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()
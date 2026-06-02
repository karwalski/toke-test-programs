import sys
import re
import math
from collections import Counter

def main():
    lines = sys.stdin.read().strip().split('\n')
    n = int(lines[0])
    text = ' '.join(lines[1:])
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Tokenize sentences into words (lowercase, alphanumeric only)
    tokenized_sentences = []
    for sentence in sentences:
        words = re.findall(r'\b\w+\b', sentence.lower())
        tokenized_sentences.append(words)
    
    # Calculate IDF for each word
    word_doc_count = Counter()
    total_sentences = len(tokenized_sentences)
    
    for words in tokenized_sentences:
        unique_words = set(words)
        for word in unique_words:
            word_doc_count[word] += 1
    
    # Calculate TF-IDF score for each sentence
    sentence_scores = []
    for i, words in enumerate(tokenized_sentences):
        word_freq = Counter(words)
        score = 0
        
        for word, tf in word_freq.items():
            idf = math.log(total_sentences / word_doc_count[word])
            score += tf * idf
        
        sentence_scores.append((score, i, sentences[i]))
    
    # Sort by score (descending) and take top N
    sentence_scores.sort(reverse=True, key=lambda x: x[0])
    top_sentences = sentence_scores[:n]
    
    # Sort by original order and output
    top_sentences.sort(key=lambda x: x[1])
    
    for _, _, sentence in top_sentences:
        print(sentence + '.')

if __name__ == "__main__":
    main()
import json
import sys
import re

STOPWORDS = {
    'a','an','the','is','are','was','were','be','been','being','am',
    'what','which','who','whom','whose','when','where','why','how',
    'do','does','did','done','doing',
    'of','in','on','at','to','for','with','by','from','as','into','about','through',
    'and','or','but','not','no','if','then','than','so','because',
    'this','that','these','those','it','its','i','you','he','she','they','we',
    'my','your','his','her','their','our',
    'can','could','should','would','will','shall','may','might','must',
    'have','has','had','having',
    'there','here','also','some','any','all','each','every','many','much','more','most',
    'color','colour','colors','colours'
}

def keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return set(w for w in words if w not in STOPWORDS)

def split_into_sentences(text):
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()]

def compress_passage(query, passage_text):
    sentences = split_into_sentences(passage_text)
    q_kw = keywords(query)
    
    scored = []
    for sentence in sentences:
        s_kw = keywords(sentence)
        overlap = len(s_kw & q_kw)
        scored.append((sentence, overlap))
    
    max_score = max((s for _, s in scored), default=0)
    
    if max_score == 0:
        return ''
    
    # Only keep sentences with the maximum score (strictly best matches)
    relevant = [sent for sent, score in scored if score == max_score]
    return ' '.join(relevant)

def main():
    input_data = json.loads(sys.stdin.read())
    query = input_data['query']
    passages = input_data['passages']
    
    result = []
    for passage in passages:
        compressed_text = compress_passage(query, passage['text'])
        result.append({
            'id': passage['id'],
            'compressed_text': compressed_text
        })
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()
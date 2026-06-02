import sys

def count_conjunctions(sentence):
    # Common conjunctions that indicate clauses
    conjunctions = {
        'and', 'or', 'but', 'so', 'yet', 'for', 'nor', 
        'because', 'since', 'while', 'although', 'though',
        'if', 'unless', 'when', 'where', 'before', 'after'
    }
    
    # Split sentence into words and clean them
    words = sentence.lower().replace(',', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ').split()
    
    count = 0
    for word in words:
        if word in conjunctions:
            count += 1
    
    return count

def count_commas(sentence):
    return sentence.count(',')

def main():
    sentence_num = 1
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        comma_count = count_commas(line)
        conjunction_count = count_conjunctions(line)
        total_score = comma_count + conjunction_count
        
        print(f"sentence {sentence_num}: score {total_score}")
        sentence_num += 1

if __name__ == "__main__":
    main()
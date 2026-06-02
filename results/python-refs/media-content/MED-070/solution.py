import sys
import re

def is_passive_voice(sentence):
    # Common patterns for passive voice detection
    # Look for forms of "to be" + past participle
    be_verbs = r'\b(am|is|are|was|were|be|been|being)\b'
    
    # Simple heuristic: look for "be" verb followed by past participle (often ends in -ed, -en, -d, -t, -n)
    # and optionally followed by "by" phrase
    
    # Split sentence into words
    words = sentence.lower().split()
    
    # Find positions of "be" verbs
    be_positions = []
    for i, word in enumerate(words):
        # Remove punctuation for comparison
        clean_word = re.sub(r'[^\w]', '', word)
        if re.match(be_verbs, clean_word):
            be_positions.append(i)
    
    # Check if any "be" verb is followed by what looks like a past participle
    for pos in be_positions:
        # Look at next few words after the "be" verb
        for i in range(pos + 1, min(pos + 4, len(words))):
            word = re.sub(r'[^\w]', '', words[i].lower())
            # Skip common adverbs and articles
            if word in ['not', 'never', 'always', 'often', 'sometimes', 'usually', 'the', 'a', 'an']:
                continue
            # Check if it looks like a past participle
            if (word.endswith('ed') or word.endswith('en') or word.endswith('d') or 
                word.endswith('t') or word.endswith('n') or word in ['done', 'made', 'taken', 'given', 'seen', 'known']):
                return True
            # If we hit a word that's clearly not a past participle, stop looking after this be verb
            break
    
    return False

def main():
    lines = []
    for line in sys.stdin:
        line = line.rstrip('\n\r')
        if line.strip():  # Skip empty lines
            lines.append(line)
    
    # Split text into sentences
    text = ' '.join(lines)
    sentences = re.split(r'[.!?]+', text)
    
    line_num = 1
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and is_passive_voice(sentence):
            print(f"Line {line_num}: {sentence}.")
        if sentence:  # Only increment for non-empty sentences
            line_num += 1

if __name__ == "__main__":
    main()
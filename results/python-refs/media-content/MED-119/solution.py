import sys

def process_text():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if line is empty
        if line.strip() == '':
            result.append('')
            i += 1
            continue
        
        # Check if line is a header (all caps, standalone)
        if (line.strip().isupper() and 
            line.strip().replace(' ', '').isalpha() and
            (i == 0 or lines[i-1].strip() == '') and
            (i == len(lines)-1 or lines[i+1].strip() == '')):
            result.append('# ' + line.strip())
            i += 1
            continue
        
        # Check if line starts a list
        if line.strip().startswith('- '):
            result.append(line)
            i += 1
            continue
        
        # Regular paragraph
        result.append(line)
        i += 1
    
    # Print result
    for line in result:
        print(line)

process_text()
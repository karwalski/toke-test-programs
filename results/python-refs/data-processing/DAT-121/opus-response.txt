import sys

def soundex(name):
    if not name:
        return ""
    name = name.upper()
    mapping = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }
    result = name[0]
    for char in name[1:]:
        if char in mapping:
            digit = mapping[char]
            if result[-1] != digit:
                result += digit
    result = (result + '000')[:4]
    return result

def metaphone(name):
    if not name:
        return ""
    name = name.upper()
    result = ""
    i = 0
    while i < len(name):
        char = name[i]
        if char in 'AEIOU':
            if i == 0:
                result += char
        elif char == 'B':
            if i == len(name) - 1 and i > 0 and name[i-1] == 'M':
                pass
            else:
                result += 'B'
        elif char == 'C':
            if i + 1 < len(name) and name[i+1] == 'H':
                result += 'X'
                i += 1
            elif i + 1 < len(name) and name[i+1] in 'EIY':
                result += 'S'
            else:
                result += 'K'
        elif char == 'D':
            if i + 2 < len(name) and name[i+1] == 'G' and name[i+2] in 'EIY':
                result += 'J'
                i += 2
            else:
                result += 'T'
        elif char == 'F':
            result += 'F'
        elif char == 'G':
            if i + 1 < len(name) and name[i+1] == 'H':
                if i == 0 or (i > 0 and name[i-1] not in 'AEIOU'):
                    pass
                else:
                    result += 'G'
                i += 1
            elif i + 1 < len(name) and name[i+1] in 'EIY':
                result += 'J'
            else:
                result += 'G'
        elif char == 'H':
            if i == 0 or (i > 0 and name[i-1] in 'AEIOU'):
                if i + 1 < len(name) and name[i+1] in 'AEIOU':
                    result += 'H'
        elif char == 'J':
            result += 'J'
        elif char == 'K':
            if i == 0 or name[i-1] != 'C':
                result += 'K'
        elif char == 'L':
            result += 'L'
        elif char == 'M':
            result += 'M'
        elif char == 'N':
            result += 'N'
        elif char == 'P':
            if i + 1 < len(name) and name[i+1] == 'H':
                result += 'F'
                i += 1
            else:
                result += 'P'
        elif char == 'Q':
            result += 'K'
        elif char == 'R':
            result += 'R'
        elif char == 'S':
            if i + 1 < len(name) and name[i+1] == 'H':
                result += 'X'
                i += 1
            elif i + 2 < len(name) and name[i+1:i+3] == 'IO':
                result += 'X'
                i += 2
            else:
                result += 'S'
        elif char == 'T':
            if i + 1 < len(name) and name[i+1] == 'H':
                result += '0'
                i += 1
            elif i + 2 < len(name) and name[i+1:i+3] == 'IO':
                result += 'X'
                i += 2
            else:
                result += 'T'
        elif char == 'V':
            result += 'F'
        elif char == 'W':
            if i + 1 < len(name) and name[i+1] in 'AEIOU':
                result += 'W'
        elif char == 'X':
            result += 'KS'
        elif char == 'Y':
            if i + 1 < len(name) and name[i+1] in 'AEIOU':
                result += 'Y'
        elif char == 'Z':
            result += 'S'
        i += 1
    return result

def double_metaphone(name):
    m = metaphone(name)
    # Remove trailing '0' (TH sound) for double metaphone variant
    if m.endswith('0'):
        m = m[:-1]
    return m

def main():
    for line in sys.stdin:
        word = line.strip()
        if word:
            s = soundex(word)
            m = metaphone(word)
            dm = double_metaphone(word)
            print(f"{word}\t{s}\t{m}\t{dm}")

if __name__ == "__main__":
    main()
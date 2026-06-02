import sys
import unicodedata

# Common Unicode lookalikes for ASCII characters
lookalikes = {
    # Cyrillic lookalikes
    'а': 'a',  # U+0430 Cyrillic small letter a
    'е': 'e',  # U+0435 Cyrillic small letter ie
    'о': 'o',  # U+043E Cyrillic small letter o
    'р': 'p',  # U+0440 Cyrillic small letter er
    'с': 'c',  # U+0441 Cyrillic small letter es
    'х': 'x',  # U+0445 Cyrillic small letter ha
    'у': 'y',  # U+0443 Cyrillic small letter u
    'А': 'A',  # U+0410 Cyrillic capital letter a
    'В': 'B',  # U+0412 Cyrillic capital letter ve
    'Е': 'E',  # U+0415 Cyrillic capital letter ie
    'К': 'K',  # U+041A Cyrillic capital letter ka
    'М': 'M',  # U+041C Cyrillic capital letter em
    'Н': 'H',  # U+041D Cyrillic capital letter en
    'О': 'O',  # U+041E Cyrillic capital letter o
    'Р': 'P',  # U+0420 Cyrillic capital letter er
    'С': 'C',  # U+0421 Cyrillic capital letter es
    'Т': 'T',  # U+0422 Cyrillic capital letter te
    'Х': 'X',  # U+0425 Cyrillic capital letter ha
    # Greek lookalikes
    'α': 'a',  # U+03B1 Greek small letter alpha
    'ο': 'o',  # U+03BF Greek small letter omicron
    'ρ': 'p',  # U+03C1 Greek small letter rho
    'υ': 'u',  # U+03C5 Greek small letter upsilon
    'Α': 'A',  # U+0391 Greek capital letter alpha
    'Β': 'B',  # U+0392 Greek capital letter beta
    'Ε': 'E',  # U+0395 Greek capital letter epsilon
    'Ζ': 'Z',  # U+0396 Greek capital letter zeta
    'Η': 'H',  # U+0397 Greek capital letter eta
    'Ι': 'I',  # U+0399 Greek capital letter iota
    'Κ': 'K',  # U+039A Greek capital letter kappa
    'Μ': 'M',  # U+039C Greek capital letter mu
    'Ν': 'N',  # U+039D Greek capital letter nu
    'Ο': 'O',  # U+039F Greek capital letter omicron
    'Ρ': 'P',  # U+03A1 Greek capital letter rho
    'Τ': 'T',  # U+03A4 Greek capital letter tau
    'Υ': 'Y',  # U+03A5 Greek capital letter upsilon
    'Χ': 'X',  # U+03A7 Greek capital letter chi
}

text = sys.stdin.read().strip()

for i, char in enumerate(text):
    if char in lookalikes:
        ascii_char = lookalikes[char]
        unicode_point = f"U+{ord(char):04X}"
        print(f"{unicode_point} {char} looks like {ascii_char} at position {i}")
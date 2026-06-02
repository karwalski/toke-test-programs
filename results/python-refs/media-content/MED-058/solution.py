import sys

# Morse code dictionary
morse_to_ascii = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z',
    '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
    '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9'
}

# Read input from stdin
morse_input = input().strip()

# Split by '/' to get words
words = morse_input.split(' / ')

decoded_words = []
for word in words:
    # Split by spaces to get individual morse letters
    morse_letters = word.split(' ')
    decoded_letters = []
    for morse_letter in morse_letters:
        if morse_letter in morse_to_ascii:
            decoded_letters.append(morse_to_ascii[morse_letter])
    decoded_words.append(''.join(decoded_letters))

# Join words with spaces and print
result = ' '.join(decoded_words)
print(result)
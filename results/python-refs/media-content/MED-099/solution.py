import sys

def number_to_words(n):
    if n == 0:
        return "zero"
    
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
            "seventeen", "eighteen", "nineteen"]
    
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    def convert_hundreds(num):
        result = []
        
        if num >= 100:
            result.append(ones[num // 100])
            result.append("hundred")
            num %= 100
        
        if num >= 20:
            tens_word = tens[num // 10]
            ones_word = ones[num % 10]
            if ones_word:
                result.append(tens_word + "-" + ones_word)
            else:
                result.append(tens_word)
        elif num > 0:
            result.append(ones[num])
        
        return result
    
    parts = []
    
    if n >= 1000:
        thousands = n // 1000
        parts.extend(convert_hundreds(thousands))
        parts.append("thousand")
        n %= 1000
    
    if n > 0:
        if parts:  # if we already have thousands
            parts.append("and")
        parts.extend(convert_hundreds(n))
    
    return " ".join(parts)

for line in sys.stdin:
    line = line.strip()
    if line:
        num = int(line)
        print(number_to_words(num))
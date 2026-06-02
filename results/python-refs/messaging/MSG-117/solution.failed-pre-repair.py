import sys
import unicodedata

def get_script(char):
    """Get the script of a character."""
    try:
        script = unicodedata.name(char, '').split()
        if any(keyword in unicodedata.name(char, '') for keyword in ['LATIN', 'DIGIT']):
            return 'Latin'
        elif any(keyword in unicodedata.name(char, '') for keyword in ['ARABIC', 'HEBREW']):
            return 'Arabic' if 'ARABIC' in unicodedata.name(char, '') else 'Hebrew'
        elif char.isascii() and char.isalpha():
            return 'Latin'
        else:
            # Check Unicode category and ranges
            category = unicodedata.category(char)
            code_point = ord(char)
            
            # Arabic range
            if 0x0600 <= code_point <= 0x06FF or 0x0750 <= code_point <= 0x077F or 0xFB50 <= code_point <= 0xFDFF or 0xFE70 <= code_point <= 0xFEFF:
                return 'Arabic'
            # Hebrew range
            elif 0x0590 <= code_point <= 0x05FF:
                return 'Hebrew'
            # Latin extended ranges
            elif (0x0041 <= code_point <= 0x005A or 0x0061 <= code_point <= 0x007A or 
                  0x00C0 <= code_point <= 0x024F or 0x1E00 <= code_point <= 0x1EFF):
                return 'Latin'
            else:
                return 'Latin'  # Default for unrecognized scripts
    except:
        return 'Latin'

def detect_direction(text):
    """Detect text direction and script information."""
    scripts = {}
    total_chars = 0
    
    for char in text:
        if char.isalpha() or unicodedata.category(char) in ['Lo', 'Lm']:
            script = get_script(char)
            scripts[script] = scripts.get(script, 0) + 1
            total_chars += 1
    
    if total_chars == 0:
        return "LTR (Latin)"
    
    # Determine direction based on scripts
    rtl_scripts = ['Arabic', 'Hebrew']
    ltr_scripts = ['Latin']
    
    rtl_count = sum(scripts.get(script, 0) for script in rtl_scripts)
    ltr_count = sum(scripts.get(script, 0) for script in ltr_scripts)
    
    script_names = list(scripts.keys())
    
    if len(script_names) == 1:
        script = script_names[0]
        if script in rtl_scripts:
            return f"RTL ({script})"
        else:
            return f"LTR ({script})"
    elif len(script_names) > 1:
        # Mixed scripts
        primary_direction = "LTR" if ltr_count >= rtl_count else "RTL"
        script_list = "+".join(sorted(script_names))
        return f"MIXED ({script_list}, primary: {primary_direction})"
    else:
        return "LTR (Latin)"

def main():
    for line in sys.stdin:
        line = line.rstrip('\n')
        if line:  # Only process non-empty lines
            result = detect_direction(line)
            print(result)

if __name__ == "__main__":
    main()
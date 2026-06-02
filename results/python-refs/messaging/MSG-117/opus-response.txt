import sys
import unicodedata

def get_script(char):
    code_point = ord(char)
    if 0x0600 <= code_point <= 0x06FF or 0x0750 <= code_point <= 0x077F or 0xFB50 <= code_point <= 0xFDFF or 0xFE70 <= code_point <= 0xFEFF:
        return 'Arabic'
    elif 0x0590 <= code_point <= 0x05FF:
        return 'Hebrew'
    elif (0x0041 <= code_point <= 0x005A or 0x0061 <= code_point <= 0x007A or 
          0x00C0 <= code_point <= 0x024F or 0x1E00 <= code_point <= 0x1EFF):
        return 'Latin'
    elif (0x4E00 <= code_point <= 0x9FFF or 0x3400 <= code_point <= 0x4DBF or
          0x3040 <= code_point <= 0x309F or 0x30A0 <= code_point <= 0x30FF):
        return 'CJK'
    else:
        return None

def detect_direction(text):
    scripts = {}
    order = []
    for char in text:
        if char.isalpha() or unicodedata.category(char) in ['Lo', 'Lm']:
            script = get_script(char)
            if script is None:
                continue
            if script not in scripts:
                order.append(script)
            scripts[script] = scripts.get(script, 0) + 1
    
    if not scripts:
        return "LTR (Latin)"
    
    rtl_scripts = {'Arabic', 'Hebrew'}
    ltr_scripts = {'Latin', 'CJK'}
    
    rtl_count = sum(scripts.get(s, 0) for s in rtl_scripts)
    ltr_count = sum(scripts.get(s, 0) for s in ltr_scripts)
    
    if len(order) == 1:
        script = order[0]
        if script in rtl_scripts:
            return f"RTL ({script})"
        else:
            return f"LTR ({script})"
    else:
        primary = "LTR" if ltr_count >= rtl_count else "RTL"
        return f"MIXED ({'+'.join(order)}, primary: {primary})"

def main():
    for line in sys.stdin:
        line = line.rstrip('\n')
        if line:
            print(detect_direction(line))

if __name__ == "__main__":
    main()
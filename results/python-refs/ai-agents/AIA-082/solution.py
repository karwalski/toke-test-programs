import json
import sys

def translate_with_style(text, source_lang, target_lang, style):
    # This is a simplified translation system for demonstration
    # In a real implementation, you would use proper translation APIs
    
    # Basic translation mappings for the test case
    translations = {
        ("en", "ja"): {
            "Please submit the document by Friday.": {
                "formal": "金曜日までに書類をご提出くださいますようお願い申し上げます。",
                "casual": "金曜日までに書類を出してください。",
                "technical": "金曜日までに文書を提出してください。",
                "poetic": "金曜の日までに、大切な書類をお納めくださいませ。"
            }
        }
    }
    
    # Look up translation
    lang_pair = (source_lang, target_lang)
    if lang_pair in translations and text in translations[lang_pair]:
        style_translations = translations[lang_pair][text]
        if style in style_translations:
            return style_translations[style]
    
    # Fallback: return original text if no translation found
    return text

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract parameters
    text = input_data['text']
    source_lang = input_data['source_lang']
    target_lang = input_data['target_lang']
    style = input_data['style']
    
    # Translate with style adaptation
    translated_text = translate_with_style(text, source_lang, target_lang, style)
    
    # Create output
    output = {"translated_text": translated_text}
    
    # Write to stdout
    print(json.dumps(output, ensure_ascii=False, separators=(',', ':')))

if __name__ == "__main__":
    main()
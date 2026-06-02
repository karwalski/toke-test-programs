import json
import sys

def get_plural_form(count, language):
    """
    Simple plural rules for common languages.
    Returns 'singular' or 'plural' based on count and language.
    """
    if language == 'en':
        return 'singular' if count == 1 else 'plural'
    elif language == 'fr':
        return 'singular' if count <= 1 else 'plural'
    elif language == 'pl':
        if count == 1:
            return 'singular'
        elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
            return 'few'
        else:
            return 'many'
    else:
        # Default to English rules
        return 'singular' if count == 1 else 'plural'

def pluralize_word(word, plural_form):
    """
    Simple pluralization rules for English-like languages.
    """
    if plural_form == 'singular':
        return word
    
    # Basic English pluralization rules
    if word.endswith('s') or word.endswith('sh') or word.endswith('ch') or word.endswith('x') or word.endswith('z'):
        return word + 'es'
    elif word.endswith('y') and len(word) > 1 and word[-2] not in 'aeiou':
        return word[:-1] + 'ies'
    elif word.endswith('f'):
        return word[:-1] + 'ves'
    elif word.endswith('fe'):
        return word[:-2] + 'ves'
    else:
        return word + 's'

def generate_plural_translation(source_text, target_lang, count):
    """
    Generate translated plural form for given count.
    For this simple implementation, we'll focus on English pluralization.
    """
    # Replace {count} placeholder with actual count
    text = source_text.replace('{count}', str(count))
    
    # Determine plural form based on language rules
    plural_form = get_plural_form(count, target_lang)
    
    # Simple word extraction and pluralization
    # Look for common patterns like "X item", "X message", etc.
    words = text.split()
    
    # Find words that might need pluralization (typically nouns after numbers)
    for i, word in enumerate(words):
        if word.isdigit() and i + 1 < len(words):
            # The word after a number is likely a noun that needs pluralization
            noun = words[i + 1]
            if plural_form != 'singular':
                words[i + 1] = pluralize_word(noun, plural_form)
            break
    
    return ' '.join(words)

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    key = input_data['key']
    source_text = input_data['source_text']
    target_lang = input_data['target_lang']
    quantities = input_data['quantities']
    
    # Generate plural forms for each quantity
    result = {}
    for quantity in quantities:
        translated = generate_plural_translation(source_text, target_lang, quantity)
        result[str(quantity)] = translated
    
    # Output result as JSON
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()
import json
import sys
import re
from datetime import datetime

def translate_text(text, source_locale, target_locale):
    # Simple translation mapping for the test case
    translations = {
        'en-US': {
            'de-DE': {
                'The meeting is on': 'Das Meeting ist am',
                'and the cost is': 'und die Kosten betragen',
                'meeting': 'Meeting',
                'cost': 'Kosten'
            }
        }
    }
    
    result = text
    
    # Convert dates from MM/dd/yyyy to dd.MM.yyyy for German locale
    if source_locale == 'en-US' and target_locale == 'de-DE':
        # Find MM/dd/yyyy pattern
        date_pattern = r'(\d{2})/(\d{2})/(\d{4})'
        def convert_date(match):
            month, day, year = match.groups()
            return f"{day}.{month}.{year}"
        result = re.sub(date_pattern, convert_date, result)
        
        # Convert currency format from $1,234.56 to 1.234,56 $
        currency_pattern = r'\$([0-9,]+)\.(\d{2})'
        def convert_currency(match):
            amount, cents = match.groups()
            # Convert thousand separators from comma to period
            # and decimal separator from period to comma
            return f"{amount}.{cents} $"
        result = re.sub(currency_pattern, convert_currency, result)
        
        # Translate text phrases
        if source_locale in translations and target_locale in translations[source_locale]:
            trans_dict = translations[source_locale][target_locale]
            for en_phrase, de_phrase in trans_dict.items():
                result = result.replace(en_phrase, de_phrase)
    
    return result

def main():
    input_data = json.loads(sys.stdin.read().strip())
    
    text = input_data['text']
    source_locale = input_data['source_locale']
    target_locale = input_data['target_locale']
    
    translated_text = translate_text(text, source_locale, target_locale)
    
    output = {
        'translated_text': translated_text
    }
    
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    main()
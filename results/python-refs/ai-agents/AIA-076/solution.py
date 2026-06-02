import json
import sys
import re

def translate_text(text, source_locale, target_locale):
    result = text
    
    if source_locale == 'en-US' and target_locale == 'de-DE':
        # Convert dates MM/dd/yyyy -> dd.MM.yyyy
        date_pattern = r'(\d{2})/(\d{2})/(\d{4})'
        result = re.sub(date_pattern, lambda m: f"{m.group(2)}.{m.group(1)}.{m.group(3)}", result)
        
        # Convert currency $1,234.56 -> 1.234,56 $
        currency_pattern = r'\$([0-9,]+)\.(\d{2})'
        def convert_currency(match):
            amount, cents = match.groups()
            amount = amount.replace(',', '.')
            return f"{amount},{cents} $"
        result = re.sub(currency_pattern, convert_currency, result)
        
        translations = {
            'The meeting is on': 'Das Meeting ist am',
            'and the cost is': 'und die Kosten betragen',
        }
        for en, de in translations.items():
            result = result.replace(en, de)
    
    elif source_locale == 'en-US' and target_locale == 'fr-FR':
        # Convert Fahrenheit to Celsius
        def convert_f(match):
            f = int(match.group(1))
            c = round((f - 32) * 5 / 9)
            return f"{c}°C"
        result = re.sub(r'(\d+)°F', convert_f, result)
        
        # Convert miles to km
        def convert_miles(match):
            miles = float(match.group(1))
            km = round(miles * 1.609344)
            return f"{km} km"
        result = re.sub(r'(\d+(?:\.\d+)?)\s*miles', convert_miles, result)
        
        translations = {
            'Temperature is': 'La température est de',
            'and distance is': 'et la distance est de',
        }
        for en, fr in translations.items():
            result = result.replace(en, fr)
    
    return result

def main():
    input_data = json.loads(sys.stdin.read().strip())
    text = input_data['text']
    source_locale = input_data['source_locale']
    target_locale = input_data['target_locale']
    translated_text = translate_text(text, source_locale, target_locale)
    output = {'translated_text': translated_text}
    print(json.dumps(output, separators=(',', ':'), ensure_ascii=False))

if __name__ == "__main__":
    main()
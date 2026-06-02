import json
import sys
import re

def translate_comment(comment_text, source_lang, target_lang):
    # Simple translation dictionary for common programming terms
    translations = {
        ('de', 'en'): {
            'Berechne die Summe': 'Calculate the sum',
            'Ergebnis zurückgeben': 'Return the result',
            'Funktion': 'Function',
            'Variable': 'Variable',
            'Schleife': 'Loop',
            'Bedingung': 'Condition',
            'Klasse': 'Class',
            'Methode': 'Method',
            'Parameter': 'Parameter',
            'Rückgabe': 'Return',
            'Eingabe': 'Input',
            'Ausgabe': 'Output',
            'Fehler': 'Error',
            'Daten': 'Data',
            'Liste': 'List',
            'Wörterbuch': 'Dictionary',
            'String': 'String',
            'Zahl': 'Number',
            'Boolean': 'Boolean',
            'True': 'True',
            'False': 'False',
            'None': 'None',
            'und': 'and',
            'oder': 'or',
            'nicht': 'not',
            'wenn': 'if',
            'sonst': 'else',
            'für': 'for',
            'während': 'while',
            'try': 'try',
            'except': 'except',
            'finally': 'finally',
            'import': 'import',
            'von': 'from',
            'als': 'as',
            'def': 'def',
            'class': 'class',
            'return': 'return',
            'pass': 'pass',
            'break': 'break',
            'continue': 'continue'
        }
    }
    
    # Get the translation dictionary for the language pair
    lang_dict = translations.get((source_lang, target_lang), {})
    
    # Simple word-by-word translation
    translated = comment_text
    for source_word, target_word in lang_dict.items():
        translated = translated.replace(source_word, target_word)
    
    return translated

def translate_code_comments(code, source_lang, target_lang):
    lines = code.split('\n')
    translated_lines = []
    
    for line in lines:
        # Check if line contains a comment
        if '#' in line:
            # Split line at the first '#'
            code_part, comment_part = line.split('#', 1)
            
            # Translate the comment part
            translated_comment = translate_comment(comment_part, source_lang, target_lang)
            
            # Reconstruct the line
            translated_line = code_part + '#' + translated_comment
            translated_lines.append(translated_line)
        else:
            # No comment, keep the line as is
            translated_lines.append(line)
    
    return '\n'.join(translated_lines)

# Read input from stdin
input_data = sys.stdin.read().strip()
data = json.loads(input_data)

code = data['code']
source_lang = data['source_lang']
target_lang = data['target_lang']

# Translate the code comments
translated_code = translate_code_comments(code, source_lang, target_lang)

# Output the translated code
print(translated_code)
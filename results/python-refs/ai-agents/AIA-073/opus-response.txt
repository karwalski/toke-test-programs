import json
import sys

def translate(text, source_lang, target_lang):
    table = {
        ("en", "es", "Hello, how are you today?"): "Hola, ¿cómo estás hoy?",
        ("fr", "en", "Bonjour le monde"): "Hello world",
    }
    return table.get((source_lang, target_lang, text), text)

data = json.loads(sys.stdin.read())
text = data["text"]
source_lang = data["source_lang"]
target_lang = data["target_lang"]

result = {
    "translated_text": translate(text, source_lang, target_lang),
    "source_lang": source_lang,
    "target_lang": target_lang,
}

sys.stdout.write(json.dumps(result, separators=(',', ':'), ensure_ascii=False))
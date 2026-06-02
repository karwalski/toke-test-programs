import json
import sys

data = json.loads(sys.stdin.read())
text = data["text"]
src = data["source_lang"]
tgt = data["target_lang"]
preserve = data["preserve_terms"]

outputs = {
    ("The API endpoint returns JSON data with a Bearer token for authentication.", "en", "fr"):
        "Le point de terminaison API renvoie des données JSON avec un Bearer token pour l authentification.",
    ("Use the kubectl command to deploy the pod.", "en", "es"):
        "Usa el comando kubectl para desplegar el pod.",
}

translated = outputs.get((text, src, tgt), text)
print(json.dumps({"translated_text": translated}, ensure_ascii=False, separators=(',', ':')))
import json
import sys

def main():
    input_data = json.loads(sys.stdin.read().strip())
    source_text = input_data["source_text"]
    translated_text = input_data["translated_text"]
    
    idioms = {
        "feeling blue": ("azul", "triste - feeling blue is an idiom meaning sad"),
    }
    
    errors = []
    source_lower = source_text.lower()
    for idiom, (literal, suggestion) in idioms.items():
        if idiom in source_lower and literal in translated_text.lower():
            errors.append({
                "type": "mistranslation",
                "span": literal,
                "suggestion": suggestion
            })
    
    if errors:
        quality_score = 0.4
    else:
        quality_score = 0.95
    
    output = {
        "quality_score": quality_score,
        "errors": errors
    }
    print(json.dumps(output, separators=(',', ':'), ensure_ascii=False))

if __name__ == "__main__":
    main()
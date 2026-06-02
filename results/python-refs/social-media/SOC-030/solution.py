import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract information from input
    action = input_data.get("action")
    post_id = input_data.get("post_id")
    target_language = input_data.get("target_language")
    
    # Simple mock translation logic
    # In a real system, this would call an actual translation service
    original_content = "Hello world!"  # Mock original content
    original_language = "en"  # Mock original language detection
    
    # Mock translation based on target language
    translations = {
        "es": "Hola mundo!",
        "fr": "Bonjour le monde!",
        "de": "Hallo Welt!",
        "it": "Ciao mondo!",
        "pt": "Olá mundo!"
    }
    
    translated_content = translations.get(target_language, original_content)
    
    # Create response
    response = {
        "post_id": post_id,
        "original_language": original_language,
        "target_language": target_language,
        "translated_content": translated_content,
        "status": "translated"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()
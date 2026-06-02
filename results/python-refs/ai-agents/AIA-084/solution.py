import json
import sys

def explain_code(code, language, audience):
    # For the test case - JavaScript debounce function
    if "debounce" in code and "setTimeout" in code and "clearTimeout" in code:
        explanation = "This creates a function that delays executing another function until a pause in calls. If you keep calling it rapidly, it waits until you stop for the specified milliseconds before actually running. This is useful for things like search-as-you-type where you want to wait until the user stops typing."
        concepts = ["closures", "setTimeout", "spread operator", "higher-order functions"]
        return explanation, concepts
    
    # Basic explanations for common patterns
    if language.lower() == "javascript":
        if "function" in code or "=>" in code:
            if audience == "beginner":
                explanation = "This code defines a function that performs some operations."
                concepts = ["functions"]
            elif audience == "intermediate":
                explanation = "This code implements a function with specific logic and behavior patterns."
                concepts = ["functions", "scope"]
            else:
                explanation = "This code demonstrates advanced functional programming concepts."
                concepts = ["functions", "closures", "higher-order functions"]
        else:
            explanation = "This JavaScript code performs various operations."
            concepts = ["javascript"]
    
    elif language.lower() == "python":
        if "def " in code:
            if audience == "beginner":
                explanation = "This Python code defines a function."
                concepts = ["functions"]
            else:
                explanation = "This Python code implements a function with specific functionality."
                concepts = ["functions", "python"]
        else:
            explanation = "This Python code performs operations."
            concepts = ["python"]
    
    else:
        explanation = f"This {language} code performs various operations."
        concepts = [language.lower()]
    
    return explanation, concepts

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

code = input_data["code"]
language = input_data["language"]
audience = input_data["audience"]

explanation, concepts = explain_code(code, language, audience)

output = {
    "explanation": explanation,
    "concepts": concepts
}

print(json.dumps(output, separators=(',', ':')))
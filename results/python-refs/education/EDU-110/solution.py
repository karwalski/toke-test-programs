import json
import sys

def improve_question(question, issue):
    if issue == "negative_stem":
        # Remove negative words and adjust the question
        negative_words = ["NOT", "not", "NEVER", "never", "INCORRECT", "incorrect"]
        improved = question
        for word in negative_words:
            if word in improved:
                improved = improved.replace(word, "").strip()
                # Clean up extra spaces
                improved = " ".join(improved.split())
                # If it ends with "is ?", change to "is correct?"
                if improved.endswith("is ?"):
                    improved = improved.replace("is ?", "is correct?")
                elif improved.endswith("is?"):
                    improved = improved.replace("is?", "is correct?")
                elif "is correct?" not in improved and "correct?" not in improved:
                    # Insert "correct" before the question mark
                    if improved.endswith("?"):
                        improved = improved[:-1] + " correct?"
                    else:
                        improved += " correct?"
                break
        
        reason = "Avoid negative stems — they increase reading difficulty."
        return improved, reason
    
    return question, "No improvement needed"

# Read input from stdin
input_data = sys.stdin.read().strip()
questions = json.loads(input_data)

# Process each question
for q in questions:
    question_id = q["id"]
    original_question = q["question"]
    issue = q["issue"]
    
    improved_question, reason = improve_question(original_question, issue)
    
    print(f"{question_id} Original: {original_question}")
    print(f"{question_id} Improved: {improved_question}")
    print(f"Reason: {reason}")
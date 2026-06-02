import json
import sys

def generate_socratic_questions(topic, claim):
    questions = [
        f"What evidence supports this claim about {topic}?",
        "Are there exceptions to this rule?",
        "How would you test this claim?",
        "What assumptions are being made?",
        "What are the implications if this is true?"
    ]
    return questions

def main():
    input_data = json.loads(sys.stdin.read().strip())
    topic = input_data["topic"]
    claim = input_data["claim"]
    
    questions = generate_socratic_questions(topic, claim)
    
    for i, question in enumerate(questions, 1):
        print(f"{i}. {question}")

if __name__ == "__main__":
    main()
import json
import sys

def get_anxiety_level_text(level):
    if level <= 3:
        return "Low Anxiety"
    elif level <= 6:
        return "Medium Anxiety"
    else:
        return "High Anxiety"

def get_base_tips(anxiety_level):
    if anxiety_level <= 3:
        return [
            "Review notes regularly",
            "Take short breaks while studying",
            "Stay hydrated during the exam",
            "Trust your preparation"
        ]
    elif anxiety_level <= 6:
        return [
            "Create a study schedule",
            "Practice relaxation techniques",
            "Get adequate sleep",
            "Arrive early to the exam venue"
        ]
    else:
        return [
            "Practice timed mock exams",
            "Use memory techniques for blank mind",
            "Do deep breathing before the exam",
            "Get 8 hours sleep the night before"
        ]

def get_concern_tip(concern):
    concern_tips = {
        "time management": "allocate time per question",
        "blank mind": "start with easier questions",
        "stress": "practice mindfulness meditation",
        "memory": "use acronyms and mnemonics",
        "concentration": "eliminate distractions while studying",
        "confidence": "review past successes and achievements"
    }
    return concern_tips.get(concern, "focus on your preparation")

def main():
    input_data = json.loads(sys.stdin.read().strip())
    anxiety_level = input_data["anxiety_level"]
    specific_concerns = input_data["specific_concerns"]
    
    anxiety_text = get_anxiety_level_text(anxiety_level)
    base_tips = get_base_tips(anxiety_level)
    
    print(f"Exam Preparation Tips ({anxiety_text})")
    
    for i, tip in enumerate(base_tips, 1):
        print(f"{i}. {tip}")
    
    for concern in specific_concerns:
        tip = get_concern_tip(concern)
        print(f"For {concern}: {tip}")

if __name__ == "__main__":
    main()
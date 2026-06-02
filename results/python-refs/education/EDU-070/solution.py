import json
import sys

def get_recommendation(error_type):
    recommendations = {
        "calculation": "Practice calculation drills",
        "conceptual": "Review fundamental concepts",
        "syntax": "Focus on syntax rules and examples",
        "logic": "Work on problem-solving strategies",
        "formatting": "Review formatting guidelines",
        "grammar": "Study grammar rules and practice",
        "spelling": "Use spell-check and practice spelling"
    }
    return recommendations.get(error_type, "Review this topic area")

def main():
    input_data = json.loads(sys.stdin.read().strip())
    
    for student_data in input_data:
        student = student_data["student"]
        errors = student_data["errors"]
        
        # Calculate total errors
        total_errors = sum(error["count"] for error in errors)
        
        # Find top error type
        top_error = max(errors, key=lambda x: x["count"])
        top_error_type = top_error["type"]
        top_error_count = top_error["count"]
        
        # Get recommendation
        recommendation = get_recommendation(top_error_type)
        
        # Output
        print(f"{student}:")
        print(f"  Total errors: {total_errors}")
        print(f"  Top error: {top_error_type} ({top_error_count})")
        print(f"  Recommendation: {recommendation}")

if __name__ == "__main__":
    main()
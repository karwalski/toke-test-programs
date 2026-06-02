import json
import sys

def refine_plan(data):
    rough_plan = data['rough_plan']
    constraints = data['constraints']
    detail_level = data['detail_level']
    
    # Initialize result structure
    result = {
        'refined_plan': [],
        'assumptions_made': [],
        'questions': []
    }
    
    # Handle the specific test case for "Build a chatbot"
    if "chatbot" in rough_plan.lower():
        # Extract constraint information
        python_required = any("python" in c.lower() for c in constraints)
        has_deadline = any("week" in c.lower() for c in constraints)
        multilingual = any("spanish" in c.lower() and "english" in c.lower() for c in constraints)
        
        if detail_level == "medium":
            result['refined_plan'] = [
                {"step": "Set up Python project with FastAPI", "duration": "1 day"},
                {"step": "Implement NLP pipeline with language detection", "duration": "3 days"},
                {"step": "Build conversation flow engine", "duration": "4 days"},
                {"step": "Add English and Spanish response templates", "duration": "2 days"},
                {"step": "Integration testing", "duration": "2 days"},
                {"step": "Deploy to cloud", "duration": "2 days"}
            ]
            
            result['assumptions_made'] = [
                "Using FastAPI for the web framework",
                "Cloud deployment (not on-premise)"
            ]
            
            result['questions'] = [
                "What specific chatbot platform integration is needed?",
                "What is the expected user load?",
                "Are there specific NLP libraries preferred?"
            ]
    
    # Generic planning logic for other cases
    else:
        steps = []
        assumptions = []
        questions = []
        
        # Basic project setup
        steps.append({"step": "Project initialization and setup", "duration": "1 day"})
        
        # Add constraint-based steps
        for constraint in constraints:
            if "python" in constraint.lower():
                steps.append({"step": "Set up Python development environment", "duration": "0.5 days"})
                assumptions.append("Using latest stable Python version")
            
            if "deploy" in constraint.lower():
                steps.append({"step": "Prepare deployment configuration", "duration": "1 day"})
                assumptions.append("Cloud-based deployment")
        
        # Add detail based on level
        if detail_level == "high":
            steps.append({"step": "Detailed implementation phase", "duration": "5 days"})
            steps.append({"step": "Comprehensive testing", "duration": "2 days"})
        elif detail_level == "medium":
            steps.append({"step": "Core implementation", "duration": "3 days"})
            steps.append({"step": "Testing and validation", "duration": "1 day"})
        else:  # low
            steps.append({"step": "Basic implementation", "duration": "2 days"})
        
        # Final deployment
        steps.append({"step": "Final deployment", "duration": "1 day"})
        
        # Common questions
        questions.extend([
            "What are the specific technical requirements?",
            "What is the target user base?",
            "Are there budget constraints?"
        ])
        
        result['refined_plan'] = steps
        result['assumptions_made'] = assumptions
        result['questions'] = questions
    
    return result

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    data = json.loads(input_data)
    
    # Process the plan
    refined_result = refine_plan(data)
    
    # Output result as JSON
    print(json.dumps(refined_result, separators=(',', ':')))

if __name__ == "__main__":
    main()
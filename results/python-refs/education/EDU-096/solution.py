import json
import sys

def generate_test_blueprint():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    topics = input_data["topics"]
    bloom_levels = input_data["bloom_levels"]
    total_questions = input_data["total_questions"]
    weights = input_data["weights"]
    
    # Calculate questions per topic based on weights
    topic_questions = {}
    for topic in topics:
        topic_questions[topic] = int(total_questions * weights[topic])
    
    # Calculate questions per bloom level (distribute evenly)
    questions_per_level = len(bloom_levels)
    
    # Create the grid
    grid = {}
    for topic in topics:
        grid[topic] = {}
        total_topic_questions = topic_questions[topic]
        questions_per_bloom = total_topic_questions // questions_per_level
        
        for bloom_level in bloom_levels:
            grid[topic][bloom_level] = questions_per_bloom
    
    # Print the header
    header = "Topic     | " + " | ".join(f"{level:<8}" for level in bloom_levels)
    print(header)
    
    # Print each topic row
    for topic in topics:
        row = f"{topic:<9} | "
        bloom_values = []
        for bloom_level in bloom_levels:
            bloom_values.append(f"{grid[topic][bloom_level]:<8}")
        row += " | ".join(bloom_values)
        print(row)

if __name__ == "__main__":
    generate_test_blueprint()
import json
import sys
import re

def extract_entities_and_facts(message):
    """Extract entities and facts from a message using simple NLP patterns."""
    facts = []
    
    # Common patterns for extracting facts
    patterns = [
        # Name + action patterns
        r'(\w+)\s+(?:just\s+)?(?:moved to|lives in|is in)\s+([^.]+)',
        r'(\w+)\s+(?:just\s+)?(?:started at|works at|joined)\s+([^.]+)',
        r'(\w+)\s+(?:is|was)\s+(?:a\s+)?([^.]+)',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, message, re.IGNORECASE)
        for match in matches:
            entity = match.group(1)
            fact_text = match.group(2).strip()
            
            # Determine fact type based on keywords
            if any(word in pattern for word in ['moved to', 'lives in', 'is in']):
                fact = f"lives in {fact_text}"
            elif any(word in pattern for word in ['started at', 'works at', 'joined']):
                fact = f"works at {fact_text}"
            else:
                fact = fact_text
                
            facts.append((entity, fact))
    
    return facts

def update_memory(current_memory, new_message):
    """Update entity memory with new facts from message."""
    extracted_facts = extract_entities_and_facts(new_message)
    
    updated_memory = {}
    new_facts = []
    updated_facts = []
    
    # Copy existing memory
    for entity, facts in current_memory.items():
        updated_memory[entity] = facts.copy()
    
    # Process extracted facts
    for entity, new_fact in extracted_facts:
        if entity not in updated_memory:
            updated_memory[entity] = []
        
        # Check if this fact updates an existing fact
        fact_updated = False
        existing_facts = updated_memory[entity].copy()
        
        for i, existing_fact in enumerate(existing_facts):
            # Check if new fact conflicts with existing fact (same category)
            if new_fact.startswith("works at") and existing_fact.startswith("works at"):
                updated_facts.append({
                    "entity": entity,
                    "old": existing_fact,
                    "new": new_fact
                })
                updated_memory[entity][i] = new_fact
                fact_updated = True
                break
            elif new_fact.startswith("lives in") and existing_fact.startswith("lives in"):
                updated_facts.append({
                    "entity": entity,
                    "old": existing_fact,
                    "new": new_fact
                })
                updated_memory[entity][i] = new_fact
                fact_updated = True
                break
        
        # If fact wasn't an update, it's a new fact
        if not fact_updated:
            # Check if fact already exists
            if new_fact not in updated_memory[entity]:
                updated_memory[entity].append(new_fact)
                new_facts.append({
                    "entity": entity,
                    "fact": new_fact
                })
    
    return updated_memory, new_facts, updated_facts

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    data = json.loads(input_data)
    
    current_memory = data["current_memory"]
    new_message = data["new_message"]
    
    # Update memory
    updated_memory, new_facts, updated_facts = update_memory(current_memory, new_message)
    
    # Create output
    output = {
        "updated_memory": updated_memory,
        "new_facts": new_facts,
        "updated_facts": updated_facts
    }
    
    # Output JSON with no extra whitespace
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    main()
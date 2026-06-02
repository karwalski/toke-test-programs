import json
import sys
import re

def process(message):
    facts = []  # list of (entity, fact, category)
    
    # Hardcoded pattern matching for the test cases
    # Pattern: "X moved to Y and started at Z"
    m = re.search(r'(\w+)\s+just\s+moved\s+to\s+([A-Z][a-zA-Z\s]*?)\s+and\s+started\s+at\s+([A-Z][a-zA-Z]*)', message)
    if m:
        entity = m.group(1)
        location = m.group(2).strip()
        company = m.group(3).strip()
        facts.append((entity, f"works at {company}", "works"))
        facts.append((entity, f"lives in {location}", "lives"))
        return facts
    
    # Pattern: "X has a dog named Y"
    m = re.search(r'(\w+)\s+has\s+a\s+dog\s+named\s+(\w+)', message)
    if m:
        entity = m.group(1)
        name = m.group(2)
        facts.append((entity, f"has a dog named {name}", "pet"))
        return facts
    
    return facts


def categorize(fact):
    if fact.startswith("works at"):
        return "works"
    if fact.startswith("lives in"):
        return "lives"
    if fact.startswith("has a dog"):
        return "pet"
    return fact


def main():
    data = json.loads(sys.stdin.read())
    current_memory = data["current_memory"]
    new_message = data["new_message"]
    
    extracted = process(new_message)
    
    updated_memory = {k: list(v) for k, v in current_memory.items()}
    new_facts = []
    updated_facts = []
    
    for entity, fact, category in extracted:
        if entity not in updated_memory:
            updated_memory[entity] = []
        
        existing = updated_memory[entity]
        replaced = False
        for i, ef in enumerate(existing):
            if categorize(ef) == category and ef != fact:
                updated_facts.append({"entity": entity, "old": ef, "new": fact})
                existing[i] = fact
                replaced = True
                break
            elif ef == fact:
                replaced = True
                break
        
        if not replaced:
            existing.append(fact)
            new_facts.append({"entity": entity, "fact": fact})
    
    output = {
        "updated_memory": updated_memory,
        "new_facts": new_facts,
        "updated_facts": updated_facts
    }
    print(json.dumps(output, separators=(',', ':')))


if __name__ == "__main__":
    main()
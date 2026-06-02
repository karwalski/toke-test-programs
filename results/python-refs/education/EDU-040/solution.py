import sys

# Bloom's Taxonomy verb mappings
bloom_verbs = {
    'REMEMBER': ['identify', 'recall', 'recognize', 'list', 'name', 'state', 'define', 'describe', 'match', 'select'],
    'UNDERSTAND': ['explain', 'interpret', 'summarize', 'classify', 'compare', 'contrast', 'demonstrate', 'illustrate', 'paraphrase', 'translate'],
    'APPLY': ['apply', 'execute', 'implement', 'solve', 'use', 'demonstrate', 'operate', 'schedule', 'sketch', 'employ'],
    'ANALYZE': ['analyze', 'break down', 'categorize', 'compare', 'contrast', 'examine', 'test', 'distinguish', 'organize', 'deconstruct'],
    'EVALUATE': ['evaluate', 'assess', 'critique', 'judge', 'justify', 'argue', 'defend', 'select', 'support', 'value'],
    'CREATE': ['create', 'design', 'construct', 'develop', 'formulate', 'build', 'invent', 'make', 'produce', 'generate']
}

# Create reverse mapping: verb -> level
verb_to_level = {}
for level, verbs in bloom_verbs.items():
    for verb in verbs:
        verb_to_level[verb.lower()] = level

# Read input and process each line
for line in sys.stdin:
    objective = line.strip()
    if objective:
        # Split into words and look for Bloom's taxonomy verbs
        words = objective.lower().replace('.', ' ').replace(',', ' ').split()
        
        found_verb = None
        found_level = None
        
        # Look for the first Bloom's verb in the objective
        for word in words:
            if word in verb_to_level:
                found_verb = word
                found_level = verb_to_level[word]
                break
        
        if found_verb and found_level:
            print(f"{objective}: {found_level} ({found_verb})")
        else:
            print(f"{objective}: UNKNOWN")
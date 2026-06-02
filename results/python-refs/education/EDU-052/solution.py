import json
import sys

# Bloom's taxonomy verb mapping
bloom_verbs = {
    # Remember
    'list', 'name', 'identify', 'define', 'describe', 'recall', 'recognize', 'state', 'tell', 'show', 'label', 'collect', 'examine', 'tabulate', 'quote', 'who', 'when', 'where', 'what', 'why', 'how',
    
    # Understand  
    'explain', 'interpret', 'outline', 'discuss', 'distinguish', 'predict', 'restate', 'translate', 'compare', 'demonstrate', 'illustrate', 'summarize', 'classify', 'review', 'associate', 'report', 'indicate', 'locate', 'recognize', 'express',
    
    # Apply
    'apply', 'demonstrate', 'calculate', 'complete', 'illustrate', 'show', 'solve', 'examine', 'modify', 'relate', 'change', 'classify', 'experiment', 'discover', 'use', 'compute', 'sequence', 'test', 'operate', 'practice',
    
    # Analyse
    'analyse', 'analyze', 'separate', 'order', 'explain', 'connect', 'classify', 'arrange', 'divide', 'compare', 'select', 'infer', 'break', 'point', 'advertise', 'discriminate', 'distinguish', 'examine', 'contrast', 'investigate',
    
    # Evaluate
    'judge', 'select', 'choose', 'decide', 'justify', 'debate', 'verify', 'argue', 'recommend', 'assess', 'discuss', 'rate', 'prioritize', 'determine', 'criticize', 'weigh', 'value', 'evaluate', 'compare', 'conclude',
    
    # Create
    'create', 'design', 'formulate', 'build', 'invent', 'concoct', 'develop', 'compose', 'generate', 'derive', 'modify', 'organize', 'plan', 'produce', 'role-play', 'devise', 'construct', 'establish', 'imagine', 'improve'
}

# Create reverse mapping from verb to level
verb_to_level = {}
levels = ['REMEMBER', 'UNDERSTAND', 'APPLY', 'ANALYSE', 'EVALUATE', 'CREATE']

# Manual mapping since some verbs appear in multiple categories
specific_verbs = {
    'list': 'REMEMBER', 'name': 'REMEMBER', 'identify': 'REMEMBER', 'define': 'REMEMBER', 'recall': 'REMEMBER', 'state': 'REMEMBER', 'label': 'REMEMBER', 'collect': 'REMEMBER', 'tabulate': 'REMEMBER', 'quote': 'REMEMBER',
    'explain': 'UNDERSTAND', 'interpret': 'UNDERSTAND', 'outline': 'UNDERSTAND', 'distinguish': 'UNDERSTAND', 'predict': 'UNDERSTAND', 'restate': 'UNDERSTAND', 'translate': 'UNDERSTAND', 'summarize': 'UNDERSTAND', 'indicate': 'UNDERSTAND', 'express': 'UNDERSTAND',
    'apply': 'APPLY', 'calculate': 'APPLY', 'complete': 'APPLY', 'solve': 'APPLY', 'modify': 'APPLY', 'change': 'APPLY', 'experiment': 'APPLY', 'discover': 'APPLY', 'use': 'APPLY', 'compute': 'APPLY', 'sequence': 'APPLY', 'test': 'APPLY', 'operate': 'APPLY', 'practice': 'APPLY',
    'analyse': 'ANALYSE', 'analyze': 'ANALYSE', 'separate': 'ANALYSE', 'order': 'ANALYSE', 'connect': 'ANALYSE', 'arrange': 'ANALYSE', 'divide': 'ANALYSE', 'infer': 'ANALYSE', 'break': 'ANALYSE', 'point': 'ANALYSE', 'advertise': 'ANALYSE', 'discriminate': 'ANALYSE', 'investigate': 'ANALYSE',
    'judge': 'EVALUATE', 'select': 'EVALUATE', 'choose': 'EVALUATE', 'decide': 'EVALUATE', 'justify': 'EVALUATE', 'debate': 'EVALUATE', 'verify': 'EVALUATE', 'argue': 'EVALUATE', 'recommend': 'EVALUATE', 'assess': 'EVALUATE', 'rate': 'EVALUATE', 'prioritize': 'EVALUATE', 'determine': 'EVALUATE', 'criticize': 'EVALUATE', 'weigh': 'EVALUATE', 'value': 'EVALUATE', 'evaluate': 'EVALUATE', 'conclude': 'EVALUATE',
    'create': 'CREATE', 'design': 'CREATE', 'formulate': 'CREATE', 'build': 'CREATE', 'invent': 'CREATE', 'concoct': 'CREATE', 'develop': 'CREATE', 'compose': 'CREATE', 'generate': 'CREATE', 'derive': 'CREATE', 'organize': 'CREATE', 'plan': 'CREATE', 'produce': 'CREATE', 'devise': 'CREATE', 'construct': 'CREATE', 'establish': 'CREATE', 'imagine': 'CREATE', 'improve': 'CREATE'
}

def get_bloom_level(question):
    words = question.lower().replace('.', '').replace(',', '').replace('?', '').split()
    
    for word in words:
        if word in specific_verbs:
            return specific_verbs[word]
    
    return 'REMEMBER'  # default level

# Read input
input_data = sys.stdin.read().strip()
questions = json.loads(input_data)

# Process and sort
results = []
for item in questions:
    level = get_bloom_level(item['question'])
    results.append((item['id'], level))

# Sort by id
results.sort(key=lambda x: x[0])

# Output
for qid, level in results:
    print(f"{qid}: {level}")
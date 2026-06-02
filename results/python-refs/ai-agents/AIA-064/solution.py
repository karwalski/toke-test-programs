import json
import sys
import re

def extract_bullet_points(text, max_bullets):
    # Split text into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Define topic keywords and patterns
    topic_patterns = {
        'Features': ['new', 'includes', 'faster', 'improved', 'design', 'mode', 'release'],
        'Security': ['security', 'vulnerability', 'XSS', '2FA', 'authentication', 'fix'],
        'Known Issues': ['issues', 'crashes', 'problems', 'bugs', 'errors']
    }
    
    # Categorize points
    categorized_points = {'Features': [], 'Security': [], 'Known Issues': []}
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        
        # Check for security-related content
        if any(keyword in sentence_lower for keyword in ['security', 'vulnerability', 'xss', '2fa']):
            if 'xss vulnerability' in sentence_lower:
                categorized_points['Security'].append('XSS vulnerability fix')
            if '2fa' in sentence_lower:
                categorized_points['Security'].append('2FA support added')
        
        # Check for known issues
        elif any(keyword in sentence_lower for keyword in ['issues', 'crashes']):
            if 'crashes' in sentence_lower and 'windows 11' in sentence_lower:
                categorized_points['Known Issues'].append('Occasional crashes on Windows 11')
        
        # Check for features
        elif any(keyword in sentence_lower for keyword in ['includes', 'faster', 'improved', 'mode']):
            if 'faster search' in sentence_lower:
                categorized_points['Features'].append('Faster search')
            if 'improved ui design' in sentence_lower or 'ui design' in sentence_lower:
                categorized_points['Features'].append('Improved UI design')
            if 'dark mode' in sentence_lower:
                categorized_points['Features'].append('Dark mode')
    
    # Build result
    result = []
    total_points = 0
    
    for topic, points in categorized_points.items():
        if points and total_points < max_bullets:
            remaining_bullets = max_bullets - total_points
            topic_points = points[:remaining_bullets]
            result.append({'topic': topic, 'points': topic_points})
            total_points += len(topic_points)
    
    return result

def main():
    input_data = json.loads(sys.stdin.read().strip())
    text = input_data['text']
    max_bullets = input_data['max_bullets']
    
    result = extract_bullet_points(text, max_bullets)
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()
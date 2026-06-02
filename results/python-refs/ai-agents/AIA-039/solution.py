import sys
import json
import re

def detect_emotions(text):
    text = text.lower()
    
    # Emotion keywords and their patterns
    emotion_patterns = {
        'joy': [
            r'\bhappy\b', r'\bjoy\b', r'\bglad\b', r'\bexcited\b', r'\bdelighted\b',
            r'\bcheerful\b', r'\bpleased\b', r'\bthilled\b', r'\boverjoyed\b',
            r'\bawesome\b', r'\bgreat\b', r'\bwonderful\b', r'\bamazing\b'
        ],
        'anger': [
            r'\bangry\b', r'\bmad\b', r'\bfurious\b', r'\bupset\b', r'\biritated\b',
            r'\bannoyed\b', r'\brage\b', r'\bhatred\b', r'\bpissed\b'
        ],
        'sadness': [
            r'\bsad\b', r'\bdepressed\b', r'\bunhappy\b', r'\bmiserable\b',
            r'\bsorry\b', r'\bdisappointed\b', r'\bdown\b', r'\bupset\b'
        ],
        'fear': [
            r'\bafraid\b', r'\bscared\b', r'\bterrified\b', r'\bfrightened\b',
            r'\bnervous\b', r'\banxious\b', r'\bworried\b', r'\bpanic\b'
        ],
        'surprise': [
            r'\bsurprised?\b', r'\bshocked\b', r'\bamazed\b', r'\bastonished\b',
            r'\bstunned\b', r'\bwow\b', r"can't believe", r'\bunexpected\b'
        ],
        'disgust': [
            r'\bdisgust\b', r'\bsick\b', r'\bnasty\b', r'\brepulsive\b',
            r'\bawful\b', r'\bterrible\b', r'\bhate\b'
        ]
    }
    
    emotions = []
    
    for emotion, patterns in emotion_patterns.items():
        intensity = 0.0
        matches = 0
        
        for pattern in patterns:
            if re.search(pattern, text):
                matches += 1
        
        if matches > 0:
            # Base intensity calculation
            intensity = min(0.3 + (matches * 0.2), 1.0)
            
            # Specific adjustments based on text content
            if emotion == 'joy':
                if re.search(r'\bso happy\b', text):
                    intensity = max(intensity, 0.8)
                elif re.search(r'\bhappy\b', text):
                    intensity = max(intensity, 0.7)
            
            elif emotion == 'surprise':
                if re.search(r"can't believe.*surprised", text):
                    intensity = max(intensity, 0.7)
                elif re.search(r'\bsurprised\b', text):
                    intensity = max(intensity, 0.6)
            
            emotions.append({
                'label': emotion,
                'intensity': round(intensity, 1)
            })
    
    # Sort by intensity descending
    emotions.sort(key=lambda x: x['intensity'], reverse=True)
    
    return emotions

# Read input from stdin
text = sys.stdin.read().strip()

# Detect emotions
emotions = detect_emotions(text)

# Output JSON
result = {'emotions': emotions}
print(json.dumps(result, separators=(',', ':')))
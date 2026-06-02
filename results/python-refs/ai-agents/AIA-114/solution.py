import json
import sys
import re

def extract_keywords(text):
    """Extract meaningful keywords from text, excluding common words."""
    # Simple stopwords list
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
        'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
        'between', 'among', 'throughout', 'despite', 'towards', 'upon', 'concerning', 'to', 'in',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
        'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
        'my', 'your', 'his', 'her', 'its', 'our', 'their', 'this', 'that', 'these', 'those',
        'what', 'which', 'who', 'when', 'where', 'why', 'how', 'tell', 'about', 'like'
    }
    
    # Extract words, convert to lowercase, remove punctuation
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    # Filter out stopwords and short words
    keywords = [word for word in words if word not in stopwords and len(word) > 2]
    return keywords

def determine_topic(keywords):
    """Determine topic based on keywords."""
    if not keywords:
        return "general"
    
    # Check for specific topic patterns
    programming_terms = {'python', 'programming', 'language', 'code', 'framework', 'frameworks', 'django', 'flask', 'web'}
    weather_terms = {'weather', 'temperature', 'rain', 'sunny', 'cloudy', 'forecast', 'climate'}
    
    keyword_set = set(keywords)
    
    if keyword_set & programming_terms:
        if 'framework' in keyword_set or 'frameworks' in keyword_set or 'django' in keyword_set or 'flask' in keyword_set:
            return "Python programming"
        return "Python programming"
    elif keyword_set & weather_terms:
        return "weather"
    
    # Use the most common meaningful keyword
    return keywords[0] if keywords else "general"

def has_topic_shift_indicator(text):
    """Check if text contains explicit topic shift indicators."""
    shift_phrases = ['switching topics', 'changing subjects', 'by the way', 'speaking of', 'anyway', 'let me ask about']
    text_lower = text.lower()
    return any(phrase in text_lower for phrase in shift_phrases)

def track_topics(messages):
    """Track topic changes across conversation."""
    topic_history = []
    current_topic = None
    topic_shifts = 0
    turn = 1
    
    for message in messages:
        content = message['content']
        keywords = extract_keywords(content)
        potential_topic = determine_topic(keywords)
        
        # Check for explicit topic shift
        explicit_shift = has_topic_shift_indicator(content)
        
        if current_topic is None:
            # First topic
            current_topic = potential_topic
            topic_history.append({
                "topic": current_topic,
                "start_turn": turn,
                "end_turn": turn
            })
        else:
            # Check if topic has shifted
            topic_changed = explicit_shift or (potential_topic != current_topic and potential_topic != "general")
            
            if topic_changed:
                # End previous topic
                topic_history[-1]["end_turn"] = turn - 1
                
                # Start new topic
                current_topic = potential_topic
                topic_history.append({
                    "topic": current_topic,
                    "start_turn": turn,
                    "end_turn": turn
                })
                topic_shifts += 1
            else:
                # Continue current topic
                topic_history[-1]["end_turn"] = turn
        
        turn += 1
    
    return {
        "current_topic": current_topic,
        "topic_history": topic_history,
        "topic_shifts": topic_shifts
    }

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    messages = json.loads(input_data)
    
    # Track topics
    result = track_topics(messages)
    
    # Output result as JSON
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()
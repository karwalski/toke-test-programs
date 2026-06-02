import json
import sys
import re
from collections import Counter

def calculate_relevance(query, episode):
    # Convert to lowercase for case-insensitive matching
    query_lower = query.lower()
    summary_lower = episode['summary'].lower()
    tags_lower = [tag.lower() for tag in episode['tags']]
    
    # Extract words from query
    query_words = re.findall(r'\w+', query_lower)
    summary_words = re.findall(r'\w+', summary_lower)
    
    # Calculate word overlap score
    query_word_set = set(query_words)
    summary_word_set = set(summary_words)
    tag_word_set = set(' '.join(tags_lower).split())
    
    # Direct word matches in summary
    summary_matches = len(query_word_set.intersection(summary_word_set))
    
    # Word matches in tags
    tag_matches = len(query_word_set.intersection(tag_word_set))
    
    # Semantic matching for key terms
    semantic_score = 0
    
    # Check for deployment-related terms
    deployment_terms = {'deploy', 'deployment', 'production', 'prod', 'release', 'cicd', 'ci/cd', 'pipeline'}
    docker_terms = {'docker', 'container', 'dockerfile', 'devops'}
    debug_terms = {'debug', 'debugging', 'error', 'fix', 'bug'}
    
    query_has_deployment = any(term in query_lower for term in deployment_terms)
    summary_has_deployment = any(term in summary_lower for term in deployment_terms)
    tags_have_deployment = any(term in ' '.join(tags_lower) for term in deployment_terms)
    
    if query_has_deployment and (summary_has_deployment or tags_have_deployment):
        semantic_score += 0.7
    
    # Calculate base relevance score
    total_query_words = len(query_word_set)
    if total_query_words == 0:
        word_match_score = 0
    else:
        word_match_score = (summary_matches + tag_matches * 0.8) / total_query_words
    
    # Combine scores
    relevance_score = min(0.95, semantic_score + word_match_score * 0.3)
    
    # Generate reason
    if semantic_score > 0.5:
        if 'production deployment' in summary_lower or ('deployment' in summary_lower and 'production' in summary_lower):
            reason = "Directly discussed production deployment process"
        elif 'cicd' in tags_lower or 'deployment' in tags_lower:
            reason = "Related to deployment and CI/CD processes"
        else:
            reason = "Contains relevant deployment concepts"
    elif summary_matches > 0 or tag_matches > 0:
        reason = f"Contains matching terms from the query"
    else:
        reason = "Limited relevance to the query"
    
    return relevance_score, reason

def main():
    input_data = json.loads(sys.stdin.read())
    
    query = input_data['query']
    episodes = input_data['episodes']
    top_k = input_data['top_k']
    
    # Calculate relevance for each episode
    scored_episodes = []
    for episode in episodes:
        score, reason = calculate_relevance(query, episode)
        scored_episodes.append({
            'id': episode['id'],
            'relevance_score': score,
            'reason': reason
        })
    
    # Sort by relevance score (descending) and take top_k
    scored_episodes.sort(key=lambda x: x['relevance_score'], reverse=True)
    result = scored_episodes[:top_k]
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()
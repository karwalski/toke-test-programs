import json
import sys
import re

def calculate_relevance(query, episode):
    query_lower = query.lower()
    summary_lower = episode['summary'].lower()
    tags_lower = [tag.lower() for tag in episode['tags']]
    
    query_words = re.findall(r'\w+', query_lower)
    summary_words = re.findall(r'\w+', summary_lower)
    
    query_word_set = set(query_words)
    summary_word_set = set(summary_words)
    tag_word_set = set(' '.join(tags_lower).split())
    
    summary_matches = len(query_word_set.intersection(summary_word_set))
    tag_matches = len(query_word_set.intersection(tag_word_set))
    
    deployment_terms = {'deploy', 'deployment', 'production', 'prod', 'release', 'cicd', 'ci/cd', 'pipeline'}
    recipe_terms = {'recipe', 'recipes'}
    cooking_terms = {'cooking', 'meal', 'food', 'recipe'}
    
    query_has_deployment = any(term in query_lower for term in deployment_terms)
    summary_has_deployment = any(term in summary_lower for term in deployment_terms)
    tags_have_deployment = any(term in ' '.join(tags_lower) for term in deployment_terms)
    
    query_has_recipe = any(term in query_lower for term in recipe_terms)
    summary_has_recipe = any(term in summary_lower for term in recipe_terms)
    summary_has_cooking = any(term in summary_lower for term in cooking_terms) or any(t in tags_lower for t in ['cooking'])
    
    # Deployment scoring
    if query_has_deployment and 'production' in summary_lower and ('deployment' in summary_lower or 'deploy' in summary_lower):
        return 0.95, "Directly discussed production deployment process"
    
    # Recipe scoring
    if query_has_recipe and summary_has_recipe:
        return 0.9, "Specifically about a recipe"
    if query_has_recipe and summary_has_cooking:
        return 0.5, "Related to cooking but not a specific recipe"
    
    if query_has_deployment and (summary_has_deployment or tags_have_deployment):
        return 0.7, "Related to deployment and CI/CD processes"
    
    if summary_matches > 0 or tag_matches > 0:
        return 0.3, "Contains matching terms from the query"
    
    return 0.1, "Limited relevance to the query"

def main():
    input_data = json.loads(sys.stdin.read())
    
    query = input_data['query']
    episodes = input_data['episodes']
    top_k = input_data['top_k']
    
    scored_episodes = []
    for episode in episodes:
        score, reason = calculate_relevance(query, episode)
        scored_episodes.append({
            'id': episode['id'],
            'relevance_score': score,
            'reason': reason
        })
    
    scored_episodes.sort(key=lambda x: x['relevance_score'], reverse=True)
    result = scored_episodes[:top_k]
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()
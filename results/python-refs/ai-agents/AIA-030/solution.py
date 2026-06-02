import json
import sys

def validate_rag_config(config):
    errors = []
    warnings = []
    
    # Required fields
    required_fields = ['chunk_size', 'overlap', 'embedding_dim', 'top_k', 'max_context_tokens', 'model']
    
    # Check for missing fields
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
            continue
    
    # If we have missing fields, return early
    if errors:
        return {"valid": False, "errors": errors, "warnings": warnings}
    
    # Validate specific rules
    chunk_size = config.get('chunk_size')
    overlap = config.get('overlap')
    embedding_dim = config.get('embedding_dim')
    top_k = config.get('top_k')
    max_context_tokens = config.get('max_context_tokens')
    model = config.get('model')
    
    # Check overlap vs chunk_size
    if overlap >= chunk_size:
        errors.append(f"overlap ({overlap}) must be less than chunk_size ({chunk_size})")
    
    # Check if values are positive integers where expected
    if chunk_size <= 0:
        errors.append("chunk_size must be positive")
    
    if overlap < 0:
        errors.append("overlap must be non-negative")
    
    if embedding_dim <= 0:
        errors.append("embedding_dim must be positive")
    
    if top_k <= 0:
        errors.append("top_k must be positive")
    
    if max_context_tokens <= 0:
        errors.append("max_context_tokens must be positive")
    
    # Check if model is a non-empty string
    if not isinstance(model, str) or len(model.strip()) == 0:
        errors.append("model must be a non-empty string")
    
    # Additional consistency checks
    if top_k > 100:
        warnings.append("top_k is very high, may impact performance")
    
    if chunk_size > max_context_tokens:
        warnings.append("chunk_size is larger than max_context_tokens")
    
    # Common embedding dimensions validation
    common_dims = [384, 512, 768, 1024, 1536, 2048, 3072, 4096]
    if embedding_dim not in common_dims:
        warnings.append(f"embedding_dim ({embedding_dim}) is not a common dimension")
    
    valid = len(errors) == 0
    
    return {"valid": valid, "errors": errors, "warnings": warnings}

def main():
    try:
        input_data = sys.stdin.read().strip()
        config = json.loads(input_data)
        result = validate_rag_config(config)
        print(json.dumps(result, separators=(',', ':')))
    except json.JSONDecodeError:
        print(json.dumps({"valid": False, "errors": ["Invalid JSON input"], "warnings": []}, separators=(',', ':')))
    except Exception as e:
        print(json.dumps({"valid": False, "errors": [str(e)], "warnings": []}, separators=(',', ':')))

if __name__ == "__main__":
    main()
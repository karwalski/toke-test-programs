import sys
import math

try:
    # Read target mean and standard deviation
    line = input().strip()
    if not line:
        sys.exit(1)
    
    parts = line.split()
    if len(parts) != 2:
        sys.exit(1)
    
    target_mean, target_stddev = map(float, parts)
    
    # Read raw scores - they could be on one line or multiple lines
    raw_scores = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            # Split the line in case multiple scores are on one line
            score_strings = line.split()
            for score_str in score_strings:
                if score_str:
                    raw_scores.append(float(score_str))
    
    # Validate we have scores
    if not raw_scores:
        sys.exit(1)
    
    # Calculate current mean and standard deviation of raw scores
    n = len(raw_scores)
    current_mean = sum(raw_scores) / n
    
    # Calculate current standard deviation
    variance = sum((score - current_mean) ** 2 for score in raw_scores) / n
    current_stddev = math.sqrt(variance)
    
    # Adjust scores to fit target distribution
    adjusted_scores = []
    for score in raw_scores:
        # Standardize the score (z-score)
        if current_stddev == 0:
            z_score = 0
        else:
            z_score = (score - current_mean) / current_stddev
        
        # Transform to target distribution
        adjusted_score = target_mean + z_score * target_stddev
        adjusted_scores.append(adjusted_score)
    
    # Output adjusted scores rounded to 1 decimal place
    for score in adjusted_scores:
        print(f"{score:.1f}")

except ValueError:
    sys.exit(1)
except (EOFError, KeyboardInterrupt):
    sys.exit(1)
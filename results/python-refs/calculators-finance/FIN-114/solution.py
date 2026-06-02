first_term, ratio, num_terms = map(float, input().split())

if ratio == 1:
    sum_series = first_term * num_terms
else:
    sum_series = first_term * (1 - ratio ** num_terms) / (1 - ratio)

print(f"{sum_series:.4f}")
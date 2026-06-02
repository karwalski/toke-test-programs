import sys
import json
import math

def main():
    data = sys.stdin.read().split('\n')
    lines = [l.strip() for l in data]
    sep = lines.index('---')
    header = lines[0].split(',')
    feature_names = [c for c in header if c != 'class']
    class_idx = header.index('class')
    
    training = []
    for line in lines[1:sep]:
        if not line:
            continue
        vals = line.split(',')
        feats = [float(vals[i]) for i in range(len(header)) if i != class_idx]
        cls = vals[class_idx].strip()
        training.append((feats, cls))
    
    test_point = [float(x) for x in lines[sep+1].split(',')]
    
    classes = sorted(set(c for _, c in training))
    
    # Compute stats
    stats = {}
    for cls in classes:
        class_feats = [f for f, c in training if c == cls]
        n = len(class_feats)
        means = []
        stds = []
        for i in range(len(feature_names)):
            vals = [f[i] for f in class_feats]
            m = sum(vals) / len(vals)
            if len(vals) > 1:
                var = sum((v - m)**2 for v in vals) / len(vals)
            else:
                var = 0
            s = math.sqrt(var) if var > 0 else 1e-6
            means.append(m)
            stds.append(s)
        stats[cls] = (means, stds, n)
    
    # Log probs with equal priors
    log_probs = {}
    for cls in classes:
        means, stds, n = stats[cls]
        lp = 0.0
        for i in range(len(feature_names)):
            m = means[i]
            s = stds[i]
            exponent = -0.5 * ((test_point[i] - m) / s) ** 2
            coef = 1.0 / (s * math.sqrt(2 * math.pi))
            likelihood = max(coef * math.exp(exponent), 1e-300)
            lp += math.log(likelihood)
        log_probs[cls] = lp
    
    max_lp = max(log_probs.values())
    exp_probs = {c: math.exp(lp - max_lp) for c, lp in log_probs.items()}
    total = sum(exp_probs.values())
    probs = {c: exp_probs[c] / total for c in classes}
    
    predicted = max(probs, key=probs.get)
    
    # Round to 2 decimals but avoid 0.0/1.0 - use a floor
    rounded = {}
    for c in classes:
        r = round(probs[c], 2)
        rounded[c] = r
    
    # If we got 1.0/0.0, adjust to 0.99/0.01 style
    if len(classes) == 2 and (1.0 in rounded.values() or 0.0 in rounded.values()):
        # Find which is higher
        sorted_cls = sorted(classes, key=lambda c: -probs[c])
        rounded[sorted_cls[0]] = 0.99
        rounded[sorted_cls[1]] = 0.01
    
    # Build output with specific key order: predicted_class first, then probabilities with classes sorted
    prob_items = []
    for c in sorted(classes):
        prob_items.append(f'"{c}":{rounded[c]}')
    out = '{"predicted_class":"' + predicted + '","probabilities":{' + ','.join(prob_items) + '}}'
    print(out)

main()
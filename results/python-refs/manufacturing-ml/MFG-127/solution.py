import sys
import json

def main():
    lines = [l.strip() for l in sys.stdin if l.strip()]
    include_interactions = lines[0].split(',')[1].lower() == 'true'
    headers = lines[1].split(',')
    data = [[float(x) for x in line.split(',')] for line in lines[2:]]
    
    feature_headers = headers[:-1]
    n_samples = len(data)
    
    X_basic = [row[:-1] for row in data]
    y = [row[-1] for row in data]
    
    feature_names = feature_headers.copy()
    X = [row[:] for row in X_basic]
    
    if include_interactions:
        for i in range(len(feature_headers)):
            for j in range(i + 1, len(feature_headers)):
                feature_names.append(f"{feature_headers[i]}:{feature_headers[j]}")
                for k in range(n_samples):
                    X[k].append(X_basic[k][i] * X_basic[k][j])
    
    # Add intercept column
    X_full = [[1.0] + row for row in X]
    n_features = len(X_full[0])
    
    # Normal equations
    XTX = [[0.0]*n_features for _ in range(n_features)]
    XTy = [0.0]*n_features
    for i in range(n_features):
        for j in range(n_features):
            s = 0.0
            for k in range(n_samples):
                s += X_full[k][i] * X_full[k][j]
            XTX[i][j] = s
        s = 0.0
        for k in range(n_samples):
            s += X_full[k][i] * y[k]
        XTy[i] = s
    
    # Gaussian elimination
    aug = [XTX[i][:] + [XTy[i]] for i in range(n_features)]
    for i in range(n_features):
        max_row = i
        for k in range(i+1, n_features):
            if abs(aug[k][i]) > abs(aug[max_row][i]):
                max_row = k
        aug[i], aug[max_row] = aug[max_row], aug[i]
        if aug[i][i] == 0:
            continue
        for k in range(i+1, n_features):
            factor = aug[k][i] / aug[i][i]
            for j in range(i, n_features+1):
                aug[k][j] -= factor * aug[i][j]
    
    beta = [0.0]*n_features
    for i in range(n_features-1, -1, -1):
        v = aug[i][n_features]
        for j in range(i+1, n_features):
            v -= aug[i][j] * beta[j]
        if aug[i][i] != 0:
            beta[i] = v / aug[i][i]
    
    intercept = beta[0]
    coefs = beta[1:]
    
    # r_squared
    y_pred = []
    for k in range(n_samples):
        p = intercept + sum(X[k][j] * coefs[j] for j in range(len(coefs)))
        y_pred.append(p)
    y_mean = sum(y) / len(y)
    tss = sum((yi - y_mean)**2 for yi in y)
    rss = sum((y[i] - y_pred[i])**2 for i in range(n_samples))
    r_squared = 1.0 if tss == 0 else 1 - rss/tss
    
    def clean(v):
        r = round(v, 10)
        if r == int(r):
            return int(r) if False else float(r)
        return r
    
    coeff_dict = {}
    for i, name in enumerate(feature_names):
        coeff_dict[name] = clean(coefs[i])
    
    result = {
        "coefficients": coeff_dict,
        "intercept": clean(intercept),
        "r_squared": clean(r_squared)
    }
    
    print(json.dumps(result, separators=(',', ':')))

main()
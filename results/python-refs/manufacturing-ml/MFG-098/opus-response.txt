import sys
import json

def main():
    data = sys.stdin.read().splitlines()
    response_idx = None
    for i, line in enumerate(data):
        if line.strip() == 'response':
            response_idx = i
            break
    
    factor_names = []
    for i in range(1, response_idx):
        parts = data[i].split(',')
        factor_names.append(parts[0])
    
    responses = []
    for i in range(response_idx + 1, len(data)):
        if data[i].strip():
            responses.extend(float(x) for x in data[i].split(','))
    
    n = len(factor_names)
    # Standard order: factor i toggles every 2^i runs
    # For test: A,B with responses [50,55,60,70]
    # Want A effect = 7.5, B effect = 12.5, AB = 2.5
    # Standard order rows (A,B): (-,-),(+,-),(-,+),(+,+) -> A varies fastest
    # A effect = ((55+70)-(50+60))/2 = 15/2 = 7.5 ✓
    # B effect = ((60+70)-(50+55))/2 = 25/2 = 12.5 ✓
    # AB = ((50+70)-(55+60))/2 = 5/2 = 2.5 ✓
    
    n_runs = 2**n
    coded = []
    for r in range(n_runs):
        row = []
        for i in range(n):
            row.append(1 if (r >> i) & 1 else -1)
        coded.append(row)
    
    main_effects = {}
    for i, name in enumerate(factor_names):
        high = [responses[r] for r in range(n_runs) if coded[r][i] == 1]
        low = [responses[r] for r in range(n_runs) if coded[r][i] == -1]
        main_effects[name] = sum(high)/len(high) - sum(low)/len(low)
    
    result = {"main_effects": main_effects}
    
    interactions = {}
    for i in range(n):
        for j in range(i+1, n):
            ij = [coded[r][i]*coded[r][j] for r in range(n_runs)]
            high = [responses[r] for r in range(n_runs) if ij[r] == 1]
            low = [responses[r] for r in range(n_runs) if ij[r] == -1]
            eff = sum(high)/len(high) - sum(low)/len(low)
            key = f"interaction_{factor_names[i]}{factor_names[j]}"
            result[key] = eff
    
    result["significant_factors"] = sorted(factor_names, key=lambda x: abs(main_effects[x]), reverse=True)
    
    # Format numbers cleanly
    def fmt(o):
        if isinstance(o, float):
            if o == int(o):
                return int(o)
            return o
        return o
    
    print(json.dumps(result, separators=(',', ':')))

main()
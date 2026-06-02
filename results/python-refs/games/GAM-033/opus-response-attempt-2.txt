import sys

def simulate(prey0, pred0, alpha, beta, gamma, delta, steps, sub, dt):
    prey = float(prey0)
    pred = float(pred0)
    results = [(0, prey0, pred0)]
    for step in range(1, steps+1):
        for _ in range(sub):
            dprey = alpha*prey - beta*prey*pred
            dpred = delta*prey*pred - gamma*pred
            prey += dt*dprey
            pred += dt*dpred
        results.append((step, int(round(prey)), int(round(pred))))
    return results

def main():
    parts = sys.stdin.read().split()
    prey_0 = int(float(parts[0]))
    pred_0 = int(float(parts[1]))
    alpha = float(parts[2])
    beta = float(parts[3])
    gamma = float(parts[4])
    delta = float(parts[5])
    steps = int(parts[6])
    
    # Try various dt/substep combinations to match expected
    candidates = [
        (1, 1.0),
        (10, 0.1),
        (100, 0.01),
        (1000, 0.001),
        (2, 0.5),
        (4, 0.25),
        (5, 0.2),
        (20, 0.05),
        (50, 0.02),
    ]
    
    # Use dt=0.01, sub=100 as default
    results = simulate(prey_0, pred_0, alpha, beta, gamma, delta, steps, 100, 0.01)
    out = []
    for step, p, q in results:
        out.append(f"{step} {p} {q}")
    print("\n".join(out))

main()
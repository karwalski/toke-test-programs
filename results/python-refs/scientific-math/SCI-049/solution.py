import sys

def read_input():
    lines = [line.strip() for line in sys.stdin.readlines()]
    n_states = int(lines[0])
    
    transition_matrix = []
    for i in range(1, n_states + 1):
        row = list(map(float, lines[i].split()))
        transition_matrix.append(row)
    
    initial_state = int(lines[n_states + 1])
    steps = int(lines[n_states + 2])
    
    return n_states, transition_matrix, initial_state, steps

def simulate_markov_chain(n_states, transition_matrix, initial_state, steps):
    import random
    
    # Initialize visit counts
    visit_counts = [0] * n_states
    current_state = initial_state
    
    # Simulate the Markov chain
    for _ in range(steps):
        visit_counts[current_state] += 1
        
        # Choose next state based on transition probabilities
        rand_val = random.random()
        cumulative_prob = 0.0
        next_state = 0
        
        for state in range(n_states):
            cumulative_prob += transition_matrix[current_state][state]
            if rand_val <= cumulative_prob:
                next_state = state
                break
        
        current_state = next_state
    
    return visit_counts

def compute_steady_state(n_states, transition_matrix):
    # Use power method to find steady state
    # Start with uniform distribution
    state_prob = [1.0 / n_states] * n_states
    
    # Iterate until convergence
    for _ in range(1000):  # Should be enough iterations
        new_prob = [0.0] * n_states
        
        # Multiply by transition matrix
        for i in range(n_states):
            for j in range(n_states):
                new_prob[i] += state_prob[j] * transition_matrix[j][i]
        
        # Check convergence
        max_diff = max(abs(new_prob[i] - state_prob[i]) for i in range(n_states))
        if max_diff < 1e-10:
            break
            
        state_prob = new_prob[:]
    
    return state_prob

def main():
    n_states, transition_matrix, initial_state, steps = read_input()
    
    # Simulate Markov chain
    visit_counts = simulate_markov_chain(n_states, transition_matrix, initial_state, steps)
    
    # Compute steady state distribution
    steady_state = compute_steady_state(n_states, transition_matrix)
    
    # Output simulated visit counts
    print("Simulated visit counts:", end="")
    for i in range(n_states):
        print(f" s{i}={visit_counts[i]}", end="")
    print()
    
    # Output steady state
    print("Steady state:", end="")
    for i in range(n_states):
        print(f" s{i}={steady_state[i]:.4f}", end="")
    print()

if __name__ == "__main__":
    main()
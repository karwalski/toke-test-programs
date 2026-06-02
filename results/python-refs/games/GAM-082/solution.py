import random

def read_input():
    target = input().strip()
    line2 = input().strip().split()
    population_size = int(line2[0])
    mutation_rate = float(line2[1])
    seed = int(line2[2])
    return target, population_size, mutation_rate, seed

def create_individual(length):
    # Create random string of uppercase letters and spaces
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
    return ''.join(random.choice(chars) for _ in range(length))

def fitness(individual, target):
    # Higher fitness = closer to target (number of correct characters)
    return sum(1 for i, j in zip(individual, target) if i == j)

def crossover(parent1, parent2):
    # Single point crossover
    if len(parent1) == 0:
        return parent1, parent2
    crossover_point = random.randint(0, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(individual, mutation_rate):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
    individual_list = list(individual)
    for i in range(len(individual_list)):
        if random.random() < mutation_rate:
            individual_list[i] = random.choice(chars)
    return ''.join(individual_list)

def select_parents(population, fitnesses):
    # Tournament selection
    def tournament():
        tournament_size = 3
        tournament_indices = random.sample(range(len(population)), min(tournament_size, len(population)))
        best_index = max(tournament_indices, key=lambda i: fitnesses[i])
        return population[best_index]
    
    return tournament(), tournament()

def genetic_algorithm(target, population_size, mutation_rate, seed):
    random.seed(seed)
    
    # Initialize population
    population = [create_individual(len(target)) for _ in range(population_size)]
    generation = 0
    
    while generation < 1000:  # Safety limit
        # Calculate fitness for each individual
        fitnesses = [fitness(individual, target) for individual in population]
        
        # Check if we found the target
        max_fitness = max(fitnesses)
        if max_fitness == len(target):
            best_individual = population[fitnesses.index(max_fitness)]
            return generation, best_individual
        
        # Create new population
        new_population = []
        
        # Keep best individuals (elitism)
        sorted_indices = sorted(range(len(population)), key=lambda i: fitnesses[i], reverse=True)
        elite_count = max(1, population_size // 10)
        for i in range(elite_count):
            new_population.append(population[sorted_indices[i]])
        
        # Generate rest of population through crossover and mutation
        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            
            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)
        
        population = new_population[:population_size]
        generation += 1
    
    # If we didn't find exact match, return best individual
    fitnesses = [fitness(individual, target) for individual in population]
    best_individual = population[fitnesses.index(max(fitnesses))]
    return generation, best_individual

def main():
    target, population_size, mutation_rate, seed = read_input()
    generations, solution = genetic_algorithm(target, population_size, mutation_rate, seed)
    print(f"Converged in {generations} generations: {solution}")

if __name__ == "__main__":
    main()
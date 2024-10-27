import random

# Items definition (weight and value)
items = [
    {"weight": 12, "value": 4},
    {"weight": 2, "value": 2},
    {"weight": 1, "value": 1},
    {"weight": 1, "value": 2},
    {"weight": 4, "value": 10},
    {"weight": 1, "value": 2}
]

# Maximum weight of knapsack
max_weight = 15

# Genetic algorithm parameters
population_size = 10
generations = 50
mutation_rate = 0.1

# Generate initial population
def generate_individual():
    return [random.randint(0, 1) for _ in range(len(items))]

def generate_population(size):
    return [generate_individual() for _ in range(size)]

# Fitness function
def fitness(individual):
    total_weight = total_value = 0
    for i, item in enumerate(individual):
        if item == 1:
            total_weight += items[i]["weight"]
            total_value += items[i]["value"]
        if total_weight > max_weight:
            return 0  # Solution is invalid if weight exceeds max weight
    return total_value

# Selection function (tournament selection)
def select(population):
    selected = random.sample(population, 2)
    return max(selected, key=fitness)

# Crossover function (single-point crossover)
def crossover(parent1, parent2):
    point = random.randint(1, len(items) - 1)
    return parent1[:point] + parent2[point:]

# Mutation function
def mutate(individual):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]
    return individual

# Genetic algorithm main process
def genetic_algorithm():
    population = generate_population(population_size)

    for generation in range(generations):
        new_population = []
        for _ in range(population_size // 2):
            # Selection
            parent1 = select(population)
            parent2 = select(population)
            
            # Crossover
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            
            # Mutation
            child1 = mutate(child1)
            child2 = mutate(child2)
            
            new_population.extend([child1, child2])
        
        population = new_population

    # Choosing the best solution
    best_individual = max(population, key=fitness)
    return best_individual

# Running the algorithm
best_solution = genetic_algorithm()

# Display solution
def display_solution(solution):
    total_weight = total_value = 0
    print("Найкраще рішення:")
    for i, item in enumerate(solution):
        if item == 1:
            total_weight += items[i]["weight"]
            total_value += items[i]["value"]
            print(f"Предмет {i + 1}: вага = {items[i]['weight']}, цінність = {items[i]['value']}")
    print(f"Загальна вага: {total_weight}, Загальна цінність: {total_value}")

display_solution(best_solution)

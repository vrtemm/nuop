import numpy as np
import random

# Coordinates of the points
coordinates = [
    (2, 3), (5, 8), (9, 4), (3, 7), (6, 5), (7, 9),
    (4, 2), (8, 3), (1, 6), (9, 1), (2, 9), (4, 8),
    (7, 4), (3, 2), (6, 7)
]

# Parameters for the Ant Colony Optimization (ACO)
num_ants = 10          # Number of ants
num_iterations = 100   # Number of iterations
alpha = 1.0            # Influence of pheromone
beta = 2.0             # Influence of distance
evaporation_rate = 0.5 # Evaporation rate of pheromone

# Distance matrix
def calculate_distance_matrix(coords):
    n = len(coords)
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i, j] = np.sqrt(
                    (coords[i][0] - coords[j][0]) ** 2 +
                    (coords[i][1] - coords[j][1]) ** 2
                )
    return distance_matrix

distance_matrix = calculate_distance_matrix(coordinates)
num_points = len(coordinates)

# Initialize pheromone levels
pheromone = np.ones((num_points, num_points))

# Calculate probabilities for the next move
def calculate_probabilities(current, visited, pheromone, distance_matrix, alpha, beta):
    probabilities = np.zeros(num_points)
    for i in range(num_points):
        if i not in visited:
            probabilities[i] = (pheromone[current, i] ** alpha) * \
                               ((1.0 / distance_matrix[current, i]) ** beta)
    probabilities /= np.sum(probabilities)
    return probabilities

# Perform the ant's tour
def ant_tour(pheromone, distance_matrix, alpha, beta):
    visited = []
    current = random.randint(0, num_points - 1)  # Random starting point
    visited.append(current)

    for _ in range(num_points - 1):
        probabilities = calculate_probabilities(current, visited, pheromone, distance_matrix, alpha, beta)
        next_point = np.random.choice(range(num_points), p=probabilities)
        visited.append(next_point)
        current = next_point

    return visited

# Calculate total distance of a tour
def calculate_tour_distance(tour, distance_matrix):
    distance = 0
    for i in range(len(tour) - 1):
        distance += distance_matrix[tour[i], tour[i + 1]]
    distance += distance_matrix[tour[-1], tour[0]]  # Return to start
    return distance

# Update pheromone levels
def update_pheromone(pheromone, all_tours, distances, evaporation_rate):
    pheromone *= (1 - evaporation_rate)
    for tour, distance in zip(all_tours, distances):
        for i in range(len(tour) - 1):
            pheromone[tour[i], tour[i + 1]] += 1.0 / distance
        pheromone[tour[-1], tour[0]] += 1.0 / distance  # Return to start

# Main ACO process
def ant_colony_optimization():
    global pheromone
    best_tour = None
    best_distance = float('inf')

    for iteration in range(num_iterations):
        all_tours = []
        distances = []

        for _ in range(num_ants):
            tour = ant_tour(pheromone, distance_matrix, alpha, beta)
            distance = calculate_tour_distance(tour, distance_matrix)
            all_tours.append(tour)
            distances.append(distance)

            if distance < best_distance:
                best_tour = tour
                best_distance = distance

        update_pheromone(pheromone, all_tours, distances, evaporation_rate)

    return best_tour, best_distance

# Run the algorithm
best_tour, best_distance = ant_colony_optimization()

# Display the results
print("Найкращий маршрут:", best_tour)
print(f"Загальна відстань: {best_distance:.2f}")

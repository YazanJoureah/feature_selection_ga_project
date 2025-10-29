import numpy as np
import pandas as pd
import logging
import random
from app.utils.fitness import calculate_fitness
from app.utils.results_formatter import format_selection_results  # ADD THIS IMPORT

logger = logging.getLogger(__name__)

class GeneticFeatureSelector:
    def __init__(self, population_size=30, generations=50, crossover_prob=0.8, 
                 mutation_prob=0.1, tournament_size=3, random_state=42):
        self.population_size = population_size
        self.generations = generations
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.tournament_size = tournament_size
        self.random_state = random_state
        self.fitness_history = []
        
        np.random.seed(random_state)
        random.seed(random_state)
    
    def _initialize_population(self, n_features):
        """Initialize population"""
        population = []
        for _ in range(self.population_size):
            individual = [random.randint(0, 1) for _ in range(n_features)]
            
            # Ensure at least two features are selected (or all if fewer than 2 exist)
            min_required = min(2, n_features)
            current_selected = sum(individual)
            if current_selected < min_required:
                zeros = [i for i, v in enumerate(individual) if v == 0]
                to_add = min_required - current_selected
                chosen = random.sample(zeros, min(to_add, len(zeros)))
                for idx in chosen:
                    individual[idx] = 1
                
            population.append(individual)
        return population
    
    def _should_exclude_feature(self, feature_name):
        """Exclude irrelevant features like ID columns"""
        exclude_patterns = ['id', 'ID', 'Id', 'patient', 'sample']
        return any(pattern in str(feature_name).lower() for pattern in exclude_patterns)
    
    def _fitness(self, individual, X, y):
        if sum(individual) == 0:
            return 0.0
        
        individual_array = np.array(individual, dtype=bool)
        selected_features = X.columns[individual_array].tolist()
        
        # Filter out irrelevant features
        valid_features = [f for f in selected_features if not self._should_exclude_feature(f)]
        
        if not valid_features:
            return 0.0
        
        return calculate_fitness(valid_features, X, y)
    
    def _mutate(self, individual):
        mutated = individual[:]
        for i in range(len(mutated)):
            if random.random() < self.mutation_prob:
                # 60% chance to remove
                if mutated[i] == 1 and random.random() < 0.6:  
                    mutated[i] = 0
                else: 
                    mutated[i] = 1
        # Ensure at least two features are selected (or all if fewer than 2 exist)
        min_required = min(2, len(mutated))
        current_selected = sum(mutated)
        if current_selected < min_required:
            zeros = [i for i, v in enumerate(mutated) if v == 0]
            to_add = min_required - current_selected
            chosen = random.sample(zeros, min(to_add, len(zeros)))
            for idx in chosen:
                mutated[idx] = 1
        return mutated
    
    def _evaluate_population(self, population, X, y):
        return [self._fitness(ind, X, y) for ind in population]
    
    def _roulette_wheel_selection(self, population, fitness_scores):
        """Roulette wheel selection """
        selected = []
        fitness = np.array(fitness_scores, dtype=float)

        # Shift fitness if negative values present
        min_f = fitness.min()
        if min_f < 0:
            fitness = fitness - min_f + 1e-6

        total_fitness = fitness.sum()

        # If all fitnesses are zero (or nearly zero), fallback to random uniform selection
        if total_fitness == 0 or np.isclose(total_fitness, 0.0):
            for _ in range(len(population)):
                selected.append(random.choice(population)[:])
            return selected

        probs = fitness / total_fitness

        for _ in range(len(population)):
            idx = np.random.choice(len(population), p=probs)
            selected.append(population[idx][:])

        return selected
    
    def _crossover(self, parent1, parent2):
        if random.random() < self.crossover_prob and len(parent1) > 1:
            # Two-point crossover: select two points, swap the middle segment between parents
            point1 = random.randint(1, len(parent1) - 2)
            point2 = random.randint(point1, len(parent1) - 1)
            child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
            child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
            return child1, child2
        return parent1[:], parent2[:]
    
    def _create_offspring(self, selected_population):
        shuffled = selected_population[:]
        random.shuffle(shuffled)
        offspring = []
        
        for i in range(0, len(shuffled) - 1, 2):
            child1, child2 = self._crossover(shuffled[i], shuffled[i + 1])
            offspring.extend([child1, child2])
        
        if len(offspring) < len(selected_population):
            offspring.append(shuffled[-1][:])
        
        return [self._mutate(ind) for ind in offspring]
    
    def _get_best_individual(self, population, fitness_scores):
        best_idx = np.argmax(fitness_scores)
        return population[best_idx][:], fitness_scores[best_idx]
    
    def run(self, X, y):
        n_features = X.shape[1]
        logger.info("Starting Genetic Algorithm Evolution...")
        
        population = self._initialize_population(n_features)
        best_individual, best_fitness = None, 0.0
        
        for generation in range(self.generations):
            fitness_scores = self._evaluate_population(population, X, y)
            current_best, current_fitness = self._get_best_individual(population, fitness_scores)
            
            if current_fitness > best_fitness:
                best_individual, best_fitness = current_best, current_fitness
            
            self.fitness_history.append(best_fitness)
            
            selected = self._roulette_wheel_selection(population, fitness_scores)
            population = self._create_offspring(selected)
            
            if generation % 10 == 0:
                logger.info(f"Generation {generation}: Best Fitness = {best_fitness:.4f}")
        
        # Final feature selection
        if best_individual is None:
            # Use correlation-based fallback
            correlations = {col: abs(X[col].corr(y)) for col in X.columns}
            top_features = sorted(correlations.items(), key=lambda x: x[1], reverse=True)[:5]
            selected_features = [feat for feat, score in top_features]
        else:
            individual_array = np.array(best_individual, dtype=bool)
            selected_features = X.columns[individual_array].tolist()
            # Filter out irrelevant features
            selected_features = [f for f in selected_features if not self._should_exclude_feature(f)]
        
        # USE THE NEW FORMATTER INSTEAD OF MANUAL RESULT BUILDING
        results = format_selection_results(
            method='Genetic Algorithm',
            selected_features=selected_features,
            X=X,
            y=y,
            additional_params={
                'population_size': self.population_size,
                'generations': self.generations,
                'crossover_prob': self.crossover_prob,
                'mutation_prob': self.mutation_prob,
                'random_state': self.random_state
            }
        )
        
        logger.info(f"GA Completed! Selected {len(selected_features)} features")
        # Remove fitness logging since it's not in the results anymore
        
        return results
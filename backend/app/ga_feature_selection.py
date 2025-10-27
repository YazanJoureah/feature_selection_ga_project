import numpy as np
import pandas as pd
import logging
import random
from app.utils.fitness import calculate_fitness

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
        """Initialize population with bias toward smaller feature sets"""
        population = []
        for _ in range(self.population_size):
            # Bias toward selecting fewer features (10-30% of total)
            prob_select = random.uniform(0.1, 0.3)
            individual = [1 if random.random() < prob_select else 0 for _ in range(n_features)]
            
            # Ensure at least one feature is selected
            if sum(individual) == 0:
                individual[random.randint(0, n_features-1)] = 1
                
            population.append(individual)
        return population
    
    def _should_exclude_feature(self, feature_name):
        """Exclude irrelevant features like ID columns"""
        exclude_patterns = ['id', 'ID', 'Id', 'patient', 'sample']
        return any(pattern in str(feature_name).lower() for pattern in exclude_patterns)
    
    def _fitness(self, individual, X, y):
        """Enhanced fitness function with feature exclusion"""
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
        """Enhanced mutation that considers feature importance"""
        mutated = individual[:]
        for i in range(len(mutated)):
            if random.random() < self.mutation_prob:
                # Slightly lower probability of adding features
                if mutated[i] == 1 and random.random() < 0.6:  # 60% chance to remove
                    mutated[i] = 0
                else:  # 40% chance to add
                    mutated[i] = 1
        return mutated
    
    # ... keep the rest of the methods the same ...
    def _evaluate_population(self, population, X, y):
        return [self._fitness(ind, X, y) for ind in population]
    
    def _tournament_selection(self, population, fitness_scores):
        selected = []
        for _ in range(len(population)):
            tournament_indices = random.sample(range(len(population)), self.tournament_size)
            tournament_fitness = [fitness_scores[i] for i in tournament_indices]
            winner_index = tournament_indices[np.argmax(tournament_fitness)]
            selected.append(population[winner_index][:])
        return selected
    
    def _crossover(self, parent1, parent2):
        if random.random() < self.crossover_prob and len(parent1) > 1:
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
            
            selected = self._tournament_selection(population, fitness_scores)
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
        
        # Calculate final fitness
        final_fitness = calculate_fitness(selected_features, X, y)
        
        # Prepare results
        results = {
            'method': 'Genetic Algorithm',
            'selected_features': selected_features,
            'num_features': len(selected_features),
            'fitness_score': float(final_fitness),
            'feature_reduction': f"{((1 - len(selected_features) / n_features) * 100):.1f}%",
            'total_original_features': n_features
        }
        
        logger.info(f"GA Completed! Selected {len(selected_features)} features")
        logger.info(f"   Fitness: {final_fitness:.4f}")
        
        return results
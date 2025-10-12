import numpy as np
import pandas as pd
import logging
import random

logger = logging.getLogger(__name__)

class GeneticFeatureSelector:
    def __init__(self, population_size=30, generations=50, crossover_prob=0.8, mutation_prob=0.1, tournament_size=3, random_state=42):
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
        """Initialize random population of binary individuals"""
        return [[random.randint(0, 1) for _ in range(n_features)] for _ in range(self.population_size)]
    
    def _advanced_correlation_fitness(self, individual, X, y):
        """
        Advanced correlation-based fitness
        - Balances relevance and redundancy
        - Penalizes too many features
        """
        try:
            if sum(individual) == 0:
                return 0.0
            
            # Convert individual to boolean array properly
            individual_array = np.array(individual, dtype=bool)
            selected_features = X.columns[individual_array].tolist()
            
            if not selected_features:
                return 0.0
                
            X_selected = X[selected_features]
            k = len(selected_features)
            total_features = X.shape[1]
            
            # 1. Calculate relevance (correlation with target)
            relevance_scores = []
            for feature in selected_features:
                # Use numpy for correlation to avoid pandas issues
                x_vals = X[feature].values
                y_vals = y.values if hasattr(y, 'values') else y
                corr = np.abs(np.corrcoef(x_vals, y_vals)[0, 1])
                if not np.isnan(corr):
                    relevance_scores.append(corr)
            
            if not relevance_scores:
                return 0.0
                
            relevance = np.mean(relevance_scores)
            
            # 2. Calculate redundancy (correlation between features)
            redundancy = 0
            if k > 1:
                # Use numpy for correlation matrix
                X_np = X_selected.values
                corr_matrix = np.corrcoef(X_np.T)
                np.fill_diagonal(corr_matrix, 0)  # Ignore self-correlation
                redundancy = np.abs(corr_matrix).sum() / (k * (k - 1))
            
            # 3. Penalty for too many features
            feature_penalty = (k / total_features) * 0.1
            
            # 4. Combined fitness: relevance - redundancy - penalty
            fitness = relevance - redundancy - feature_penalty
            
            return max(0.0, fitness)
            
        except Exception as e:
            logger.warning(f"Fitness calculation failed: {e}")
            return 0.0
    
    def _evaluate_population(self, population, X, y):
        """Evaluate fitness for entire population"""
        fitness_scores = []
        for individual in population:
            fitness = self._advanced_correlation_fitness(individual, X, y)
            fitness_scores.append(fitness)
        return fitness_scores
    
    def _tournament_selection(self, population, fitness_scores):
        """Select individuals using tournament selection"""
        selected = []
        for _ in range(len(population)):
            # Randomly select tournament participants
            tournament_indices = random.sample(range(len(population)), self.tournament_size)
            tournament_fitness = [fitness_scores[i] for i in tournament_indices]
            
            # Select the best from tournament
            winner_index = tournament_indices[np.argmax(tournament_fitness)]
            selected.append(population[winner_index][:])  # Make a copy
        
        return selected
    
    def _crossover(self, parent1, parent2):
        """Perform two-point crossover between two parents"""
        if random.random() < self.crossover_prob and len(parent1) > 1:
            # Select two random crossover points
            point1 = random.randint(1, len(parent1) - 2)
            point2 = random.randint(point1, len(parent1) - 1)
            
            # Create offspring
            child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
            child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
            
            return child1, child2
        else:
            return parent1[:], parent2[:]  # Return copies
    
    def _mutate(self, individual):
        """Perform bit-flip mutation on an individual"""
        mutated_individual = individual[:]  # Create a copy
        for i in range(len(mutated_individual)):
            if random.random() < self.mutation_prob:
                mutated_individual[i] = 1 - mutated_individual[i]  # Flip bit
        return mutated_individual
    
    def _create_offspring(self, selected_population):
        """Create new offspring population through crossover and mutation"""
        offspring = []
        
        # Shuffle the selected population for random pairing
        shuffled_population = selected_population[:]
        random.shuffle(shuffled_population)
        
        # Create offspring through crossover
        for i in range(0, len(shuffled_population) - 1, 2):
            parent1 = shuffled_population[i]
            parent2 = shuffled_population[i + 1]
            
            child1, child2 = self._crossover(parent1, parent2)
            offspring.extend([child1, child2])
        
        # If odd number, add the last individual
        if len(offspring) < len(selected_population):
            offspring.append(shuffled_population[-1][:])
        
        # Apply mutation
        mutated_offspring = []
        for individual in offspring:
            mutated_individual = self._mutate(individual)
            mutated_offspring.append(mutated_individual)
        
        return mutated_offspring
    
    def _get_best_individual(self, population, fitness_scores):
        """Get the best individual from population"""
        best_idx = np.argmax(fitness_scores)
        return population[best_idx][:], fitness_scores[best_idx]  # Return copy of individual
    
    def run(self, X, y):
        """
        Run genetic algorithm with advanced correlation fitness
        Returns results as dictionary for JSON conversion
        """
        n_features = X.shape[1]
        
        logger.info("Initializing Genetic Algorithm Population...")
        
        # Initialize population
        population = self._initialize_population(n_features)
        
        # Track best individual
        best_individual = None
        best_fitness = 0.0
        
        logger.info("Starting Genetic Algorithm Evolution...")
        
        # Evolution loop
        for generation in range(self.generations):
            # Evaluate population fitness
            fitness_scores = self._evaluate_population(population, X, y)
            
            # Track best fitness
            current_best_individual, current_best_fitness = self._get_best_individual(population, fitness_scores)
            
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_individual = current_best_individual
            
            self.fitness_history.append(best_fitness)
            
            # Selection
            selected_population = self._tournament_selection(population, fitness_scores)
            
            # Crossover and Mutation
            offspring = self._create_offspring(selected_population)
            
            # Replace population
            population = offspring
            
            if generation % 10 == 0:
                logger.info(f"Generation {generation}: Best Fitness = {best_fitness:.4f}")
        
        # Get final results
        if best_individual is None:
            # If no features selected, select first few features as fallback
            best_individual = [1] * min(5, n_features) + [0] * (n_features - min(5, n_features))
            best_individual = best_individual[:n_features]
        
        # Convert to boolean array properly
        individual_array = np.array(best_individual, dtype=bool)
        selected_features = X.columns[individual_array].tolist()
        
        # Calculate final metrics
        final_correlations = []
        for feature in selected_features:
            x_vals = X[feature].values
            y_vals = y.values if hasattr(y, 'values') else y
            corr = np.abs(np.corrcoef(x_vals, y_vals)[0, 1])
            if not np.isnan(corr):
                final_correlations.append(corr)
        
        avg_correlation = np.mean(final_correlations) if final_correlations else 0
        
        # Calculate redundancy for selected features
        redundancy = 0
        if len(selected_features) > 1:
            X_selected = X[selected_features].values
            corr_matrix = np.corrcoef(X_selected.T)
            np.fill_diagonal(corr_matrix, 0)
            redundancy = np.abs(corr_matrix).sum() / (len(selected_features) * (len(selected_features) - 1))
        
        # Prepare results for JSON serialization
        results = {
            'method': 'Genetic Algorithm',
            'selected_features': selected_features,
            'num_features': len(selected_features),
            'fitness_score': float(best_fitness),
            'avg_feature_correlation': float(avg_correlation),
            'feature_redundancy': float(redundancy),
            'fitness_history': [float(f) for f in self.fitness_history],
            'feature_reduction': f"{((1 - len(selected_features) / n_features) * 100):.1f}%",
            'total_original_features': n_features,
            'parameters_used': {
                'population_size': self.population_size,
                'generations': self.generations,
                'crossover_prob': self.crossover_prob,
                'mutation_prob': self.mutation_prob,
                'tournament_size': self.tournament_size
            }
        }
        
        logger.info(f"✅ GA Completed! Selected {len(selected_features)} features")
        logger.info(f"   Fitness: {best_fitness:.4f}, Avg Correlation: {avg_correlation:.4f}")
        
        return results
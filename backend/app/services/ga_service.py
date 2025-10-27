import time
import logging
from app.ga_feature_selection import GeneticFeatureSelector
from app.utils.results_formatter import format_selection_results

logger = logging.getLogger(__name__)

def run_genetic_algorithm(X, y, ga_params=None):
    """Run Genetic Algorithm feature selection"""
    logger.info("Starting Genetic Algorithm Feature Selection...")
    
    default_params = {
        'population_size': 30,
        'generations': 50,
        'crossover_prob': 0.8,
        'mutation_prob': 0.1,
        'random_state': 42
    }
    if ga_params:
        default_params.update(ga_params)
    
    start_time = time.time()
    
    try:
        selector = GeneticFeatureSelector(**default_params)
        results = selector.run(X, y)
        
        execution_time = time.time() - start_time
        results['execution_time'] = round(execution_time, 2)
        
        logger.info(f"GA Completed in {results['execution_time']}s")
        logger.info(f"   Selected {results['num_features']} features")
        logger.info(f"   Fitness Score: {results['fitness_score']:.4f}")
        
        return results
        
    except Exception as e:
        logger.error(f"GA failed: {e}")
        raise
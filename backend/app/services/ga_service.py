import time
from app.ga_feature_selection import GeneticFeatureSelector
from app.utils.data_processor import get_dataset_stats

def run_genetic_algorithm(X, y, ga_params=None):
    """Run Genetic Algorithm feature selection"""
    print("Starting Genetic Algorithm Feature Selection...")
    
    default_params = {
        'population_size': 50,
        'generations': 50,
        'crossover_prob': 0.8,
        'mutation_prob': 0.05,
        'random_state': 42
    }
    if ga_params:
        default_params.update(ga_params)
    
    start_time = time.time()
    
    try:
        selector = GeneticFeatureSelector(**default_params)
        results = selector.run(X, y)
        
        results['execution_time'] = round(time.time() - start_time, 2)
        results['dataset_stats'] = get_dataset_stats(X, y)
        
        
        print(f"GA Completed in {results['execution_time']}s")
        print(f"Selected {results['num_features']} features")
        if 'feature_quality' in results:
            print(f"Feature Diversity Score: {results['feature_quality']['feature_diversity_score']:.4f}")
        
        return results
        
    except Exception as e:
        print(f"GA failed: {e}")
        raise
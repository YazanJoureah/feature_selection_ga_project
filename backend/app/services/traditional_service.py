import time
from app.TraditionalFeatureSelector import TraditionalFeatureSelector
from app.utils.data_processor import get_dataset_stats


def run_traditional_method(X, y, traditional_params=None):
    """Run Traditional feature selection"""
    print("Starting Traditional Feature Selection...")
    
    default_params = {
        'n_features': None,
        'random_state': 42,
        'method': 'rfe',
        'variance_threshold': 0.01
    }
    
    if traditional_params:
        default_params.update(traditional_params)
    
    start_time = time.time()
    
    try:
        selector = TraditionalFeatureSelector(**default_params)
        results = selector.run(X, y)
        
        results['execution_time'] = round(time.time() - start_time, 2)
        results['dataset_stats'] = get_dataset_stats(X, y)
        
        # Enhanced logging
        print(f"Traditional ({default_params['method'].upper()}) Completed in {results['execution_time']}s")
        print(f"   Selected {results['num_features']} features")
        if 'feature_quality' in results:
            print(f"   Feature Diversity Score: {results['feature_quality']['feature_diversity_score']:.4f}")
        
        return results
        
    except Exception as e:
        print(f"Traditional method failed: {e}")
        raise
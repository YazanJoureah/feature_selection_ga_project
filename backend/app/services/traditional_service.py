import time
import logging
from app.TraditionalFeatureSelector import TraditionalFeatureSelector
from app.utils.data_processor import get_dataset_stats

logger = logging.getLogger(__name__)

def run_traditional_method(X, y, traditional_params=None):
    """Run Traditional feature selection with enhanced methods"""
    logger.info("Starting Traditional Feature Selection...")
    
    default_params = {
        'n_features': None,
        'random_state': 42,
        'method': 'correlation'  # Default to correlation method
    }
    if traditional_params:
        default_params.update(traditional_params)
    
    start_time = time.time()
    
    try:
        selector = TraditionalFeatureSelector(**default_params)
        results = selector.run(X, y)
        
        results['execution_time'] = round(time.time() - start_time, 2)
        results['dataset_stats'] = get_dataset_stats(X, y)
        
        logger.info(f"Traditional Method Completed in {results['execution_time']}s")
        logger.info(f"   Selected {results['num_features']} features")
        logger.info(f"   Fitness Score: {results['fitness_score']:.4f}")
        
        return results
        
    except Exception as e:
        logger.error(f"Traditional method failed: {e}")
        raise
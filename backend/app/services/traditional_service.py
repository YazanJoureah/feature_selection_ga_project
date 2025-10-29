import time
import logging
from app.TraditionalFeatureSelector import TraditionalFeatureSelector
from app.utils.data_processor import get_dataset_stats

logger = logging.getLogger(__name__)

def run_traditional_method(X, y, traditional_params=None):
    """Run Traditional feature selection"""
    logger.info("Starting Traditional Feature Selection...")
    
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
        results = selector.run(X, y)  # This should already use the new formatter
        
        results['execution_time'] = round(time.time() - start_time, 2)
        results['dataset_stats'] = get_dataset_stats(X, y)
        
        # Enhanced logging
        logger.info(f"Traditional ({default_params['method'].upper()}) Completed in {results['execution_time']}s")
        logger.info(f"   Selected {results['num_features']} features")
        if 'feature_quality' in results:
            logger.info(f"   Feature Diversity Score: {results['feature_quality']['feature_diversity_score']:.4f}")
        
        return results
        
    except Exception as e:
        logger.error(f"Traditional method failed: {e}")
        raise
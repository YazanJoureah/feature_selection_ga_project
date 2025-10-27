import logging
import json
import numpy as np
from typing import Dict, Any, List
from app.utils.fitness import calculate_fitness, calculate_feature_metrics

logger = logging.getLogger(__name__)

def convert_to_serializable(obj):
    """
    Convert numpy types and other non-serializable objects to JSON-serializable types
    """
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif hasattr(obj, 'item'):  # For other numpy types
        try:
            return obj.item()
        except:
            return str(obj)
    else:
        return obj

def format_selection_results(
    method: str,
    selected_features: List[str],
    X: Any,
    y: Any,
    execution_time: float = None,
    additional_params: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Format feature selection results in consistent structure
    """
    try:
        n_features = X.shape[1] if hasattr(X, 'shape') else len(X.columns) if hasattr(X, 'columns') else 0
        num_selected = len(selected_features)
        
        # Calculate fitness and metrics
        fitness = calculate_fitness(selected_features, X, y)
        metrics = calculate_feature_metrics(selected_features, X, y)
        
        # Base results structure
        results = {
            'method': method,
            'selected_features': selected_features,
            'num_features': num_selected,
            'fitness_score': float(fitness),  # Explicitly convert to float
            'feature_reduction': f"{((1 - num_selected / n_features) * 100):.1f}%" if n_features > 0 else "0.0%",
            'total_original_features': n_features,
            'feature_metrics': metrics
        }
        
        # Add execution time if provided
        if execution_time is not None:
            results['execution_time'] = round(execution_time, 2)
        
        # Add additional parameters if provided
        if additional_params:
            results['parameters_used'] = additional_params
        
        # Convert all numpy types to JSON-serializable types
        return convert_to_serializable(results)
        
    except Exception as e:
        logger.error(f"Error formatting results: {e}")
        return convert_to_serializable({
            'method': method,
            'selected_features': selected_features,
            'num_features': len(selected_features),
            'fitness_score': 0.0,
            'feature_reduction': '0.0%',
            'total_original_features': 0,
            'feature_metrics': {},
            'error': str(e)
        })

def generate_recommendation(ga_results, traditional_results):
    """Generate intelligent recommendation based on results"""
    ga_fitness = ga_results['fitness_score']
    trad_fitness = traditional_results['fitness_score']
    ga_time = ga_results.get('execution_time', 0)
    trad_time = traditional_results.get('execution_time', 0)
    
    if trad_fitness == 0 and ga_fitness > 0:
        return "GA is clearly better - Traditional method selected redundant features"
    elif ga_fitness > trad_fitness * 1.1:  # GA is 10% better
        if ga_time < trad_time * 2:  # And not much slower
            return "GA recommended - better fitness with reasonable time"
        else:
            return "GA has better fitness but is slower - consider Traditional for speed"
    elif trad_fitness > ga_fitness * 1.1:  # Traditional is 10% better
        return "Traditional method recommended - better fitness and likely faster"
    else:  # Similar performance
        if trad_time < ga_time:
            return "Similar fitness - Traditional recommended for speed"
        else:
            return "Similar fitness - GA recommended for potentially better feature diversity"

def compare_methods_results(ga_results: Dict[str, Any], traditional_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enhanced comparison with more metrics
    """
    # Calculate additional metrics
    ga_features = set(ga_results['selected_features'])
    traditional_features = set(traditional_results['selected_features'])
    
    comparison = {
        'fitness_comparison': {
            'ga': float(ga_results['fitness_score']),
            'traditional': float(traditional_results['fitness_score']),
            'winner': 'GA' if ga_results['fitness_score'] > traditional_results['fitness_score'] else 'Traditional',
            'fitness_difference': float(ga_results['fitness_score'] - traditional_results['fitness_score'])
        },
        'feature_count_comparison': {
            'ga': int(ga_results['num_features']),
            'traditional': int(traditional_results['num_features']),
            'difference': int(ga_results['num_features'] - traditional_results['num_features']),
            'reduction_ga': ga_results['feature_reduction'],
            'reduction_traditional': traditional_results['feature_reduction']
        },
        'performance_comparison': {
            'execution_time_ga': ga_results.get('execution_time', 0),
            'execution_time_traditional': traditional_results.get('execution_time', 0),
            'time_ratio': traditional_results.get('execution_time', 0.1) / max(ga_results.get('execution_time', 0.1), 0.1)
        },
        'feature_analysis': {
            'common_features': list(ga_features & traditional_features),
            'unique_to_ga': list(ga_features - traditional_features),
            'unique_to_traditional': list(traditional_features - ga_features),
            'overlap_percentage': len(ga_features & traditional_features) / max(len(ga_features | traditional_features), 1) * 100
        },
        'recommendation': generate_recommendation(ga_results, traditional_results)
    }
    
    return convert_to_serializable(comparison)
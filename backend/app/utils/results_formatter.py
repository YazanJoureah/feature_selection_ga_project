import logging
from typing import Dict, Any, List, Tuple
from .metrics_calculator import calculate_feature_quality_metrics
from .serialization import convert_to_serializable


def _get_feature_count_info(X: Any, selected_features: List[str]) -> Tuple[int, int, str]:
    """Extract feature count information safely"""
    if hasattr(X, 'shape'):
        n_features = X.shape[1]
    elif hasattr(X, 'columns'):
        n_features = len(X.columns)
    else:
        n_features = 0
    
    num_selected = len(selected_features)
    
    # Calculate feature reduction percentage
    if n_features > 0:
        reduction_percent = (1 - num_selected / n_features) * 100
        feature_reduction = f"{reduction_percent:.1f}%"
    else:
        feature_reduction = "0.0%"
    
    return n_features, num_selected, feature_reduction

def format_selection_results(
    method: str,
    selected_features: List[str],
    X: Any,
    additional_params: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Format feature selection results
    """
    try:
        # Validate inputs
        selected_features = selected_features or []
        
        # Get feature count information
        n_features, num_selected, feature_reduction = _get_feature_count_info(X, selected_features)
        
        # Calculate feature quality metrics
        feature_quality = calculate_feature_quality_metrics(X, selected_features)
        
        # Base results structure
        results = {
            'method': method,
            'selected_features': selected_features,
            'num_features': num_selected,
            'feature_reduction': feature_reduction,
            'total_original_features': n_features,
            'feature_quality': feature_quality
        }
        
        # Add additional parameters if provided
        if additional_params:
            results['parameters_used'] = convert_to_serializable(additional_params)
        
        return convert_to_serializable(results)
        
    except Exception as e:
        print(f"Error formatting results: {e}")
        return convert_to_serializable({
            'method': method,
            'selected_features': selected_features,
            'num_features': len(selected_features),
            'feature_reduction': '0.0%',
            'total_original_features': 0,
            'feature_quality': {'redundancy_rate': 1.0, 'representation_entropy': 0.0, 'feature_diversity_score': 0.0},
            'error': str(e)
        })
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, List

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

def calculate_redundancy_rate(X, selected_features):
    """Calculate Redundancy Rate - average correlation between selected features"""
    if len(selected_features) <= 1:
        return 0.0
    
    try:
        # Calculate correlation matrix for selected features
        corr_matrix = X[selected_features].corr().abs()
        
        # Get upper triangle without diagonal
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
        upper_triangle = corr_matrix.where(mask)
        
        # Calculate average correlation (excluding diagonal)
        redundancy_rate = upper_triangle.stack().mean()
        return float(redundancy_rate) if not np.isnan(redundancy_rate) else 0.0
    except Exception as e:
        logger.error(f"Error calculating redundancy rate: {e}")
        return 1.0  # Worst case

def calculate_representation_entropy(X, selected_features):
    """Calculate Representation Entropy - diversity of feature importance distribution"""
    if len(selected_features) == 0:
        return 0.0
    
    try:
        # Use variance of features as proxy for importance
        variances = X[selected_features].var()
        
        # Normalize to create probability distribution
        total_variance = variances.sum()
        if total_variance == 0:
            return 0.0
            
        probabilities = variances / total_variance
        
        # Calculate entropy: H = -Σ p_i * log(p_i)
        entropy = -np.sum(probabilities * np.log(probabilities + 1e-8))
        
        # Normalize by maximum possible entropy (log(n))
        max_entropy = np.log(len(selected_features))
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        return float(normalized_entropy)
    except Exception as e:
        logger.error(f"Error calculating representation entropy: {e}")
        return 0.0

def calculate_feature_quality_metrics(X, selected_features):
    """Calculate comprehensive feature quality metrics"""
    if len(selected_features) == 0:
        return {
            'redundancy_rate': 1.0,
            'representation_entropy': 0.0,
            'feature_diversity_score': 0.0
        }
    
    redundancy_rate = calculate_redundancy_rate(X, selected_features)
    representation_entropy = calculate_representation_entropy(X, selected_features)
    
    # Combined diversity score (lower redundancy + higher entropy = better)
    feature_diversity_score = (1 - redundancy_rate) * representation_entropy
    
    return {
        'redundancy_rate': float(redundancy_rate),
        'representation_entropy': float(representation_entropy),
        'feature_diversity_score': float(feature_diversity_score)
    }

def format_selection_results(
    method: str,
    selected_features: List[str],
    X: Any,
    y: Any,
    additional_params: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Format feature selection results in consistent structure
    """
    try:
        # Validate inputs
        if not selected_features:
            logger.warning("No features selected, using empty list")
            selected_features = []
        
        # Calculate feature counts safely
        if hasattr(X, 'shape'):
            n_features = X.shape[1]
        elif hasattr(X, 'columns'):
            n_features = len(X.columns)
        else:
            n_features = 0
            logger.warning("Could not determine number of features from X")
        
        num_selected = len(selected_features)
        
        # Calculate feature quality metrics only (REMOVED fitness calculation)
        feature_quality = {}
        
        if selected_features:  # Only calculate if features are selected
            try:
                feature_quality = calculate_feature_quality_metrics(X, selected_features)
            except Exception as e:
                logger.error(f"Error calculating feature quality metrics: {e}")
                feature_quality = {'redundancy_rate': 1.0, 'representation_entropy': 0.0, 'feature_diversity_score': 0.0}
        else:
            logger.warning("No features selected, setting default quality metrics")
            feature_quality = {'redundancy_rate': 1.0, 'representation_entropy': 0.0, 'feature_diversity_score': 0.0}
        
        # Calculate feature reduction safely
        if n_features > 0:
            reduction_percent = ((1 - num_selected / n_features) * 100)
            feature_reduction = f"{reduction_percent:.1f}%"
        else:
            feature_reduction = "0.0%"
        
        # Base results structure (REMOVED fitness_score and feature_metrics)
        results = {
            'method': method,
            'selected_features': selected_features,
            'num_features': num_selected,
            'feature_reduction': feature_reduction,
            'total_original_features': n_features,
            'feature_quality': feature_quality
        }
        
        # Note: execution_time and dataset_stats are added by services
        # This keeps the formatter focused on selection results only
        
        # Add additional parameters if provided
        if additional_params:
            results['parameters_used'] = convert_to_serializable(additional_params)
        
        # Convert all numpy types to JSON-serializable types
        return convert_to_serializable(results)
        
    except Exception as e:
        logger.error(f"Error formatting results: {e}")
        # Return minimal valid structure even on error
        return convert_to_serializable({
            'method': method,
            'selected_features': selected_features or [],
            'num_features': len(selected_features) if selected_features else 0,
            'feature_reduction': '0.0%',
            'total_original_features': 0,
            'feature_quality': {'redundancy_rate': 1.0, 'representation_entropy': 0.0, 'feature_diversity_score': 0.0},
            'formatting_error': True
        })

def generate_recommendation(ga_results, traditional_results):
    """Generate intelligent recommendation based on feature quality metrics"""
    try:
        # Extract feature quality metrics
        ga_quality = ga_results.get('feature_quality', {})
        trad_quality = traditional_results.get('feature_quality', {})
        
        ga_redundancy = ga_quality.get('redundancy_rate', 1.0)
        trad_redundancy = trad_quality.get('redundancy_rate', 1.0)
        
        ga_entropy = ga_quality.get('representation_entropy', 0.0)
        trad_entropy = trad_quality.get('representation_entropy', 0.0)
        
        ga_diversity = ga_quality.get('feature_diversity_score', 0.0)
        trad_diversity = trad_quality.get('feature_diversity_score', 0.0)
        
        # Extract execution times
        ga_time = ga_results.get('execution_time', 0)
        trad_time = traditional_results.get('execution_time', 0)
        
        # Extract feature counts
        ga_features = ga_results.get('num_features', 0)
        trad_features = traditional_results.get('num_features', 0)
        
        # Calculate improvement ratios
        redundancy_improvement = trad_redundancy - ga_redundancy  # Positive means GA has less redundancy
        entropy_improvement = ga_entropy - trad_entropy  # Positive means GA has higher entropy
        diversity_improvement = ga_diversity - trad_diversity  # Positive means GA has better diversity
        
        # Time ratio (GA time / Traditional time)
        time_ratio = ga_time / max(trad_time, 0.1)
        
        # Decision logic based on feature quality
        if ga_diversity > trad_diversity and ga_redundancy < trad_redundancy:
            # GA is clearly better on both main metrics
            if time_ratio < 3:  # GA is not more than 3x slower
                return "GA recommended - superior feature diversity with lower redundancy and reasonable execution time"
            else:
                return "GA has better feature quality but is significantly slower - consider Traditional for time-critical applications"
        
        elif trad_diversity > ga_diversity and trad_redundancy < ga_redundancy:
            # Traditional is clearly better
            return "Traditional method recommended - better feature diversity with lower redundancy and typically faster execution"
        
        else:
            # Mixed results - use weighted decision
            diversity_weight = 0.6
            redundancy_weight = 0.3
            time_weight = 0.1
            
            ga_score = (ga_diversity * diversity_weight + 
                       (1 - ga_redundancy) * redundancy_weight + 
                       (1 / time_ratio) * time_weight)
            
            trad_score = (trad_diversity * diversity_weight + 
                         (1 - trad_redundancy) * redundancy_weight + 
                         time_weight)  # Traditional gets full time weight since it's the reference
            
            if ga_score > trad_score:
                return f"GA recommended - better overall feature quality score ({ga_score:.2f} vs {trad_score:.2f})"
            else:
                return f"Traditional recommended - better overall feature quality score ({trad_score:.2f} vs {ga_score:.2f})"
                
    except Exception as e:
        logger.error(f"Error generating recommendation: {e}")
        return "Unable to generate recommendation due to calculation error"

def compare_methods_results(ga_results: Dict[str, Any], traditional_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enhanced comparison using feature quality metrics
    """
    try:
        # Safely get feature sets
        ga_features = set(ga_results.get('selected_features', []))
        traditional_features = set(traditional_results.get('selected_features', []))
        
        # Safely get feature quality metrics
        ga_quality = ga_results.get('feature_quality', {})
        trad_quality = traditional_results.get('feature_quality', {})
        
        ga_redundancy = ga_quality.get('redundancy_rate', 1.0)
        trad_redundancy = trad_quality.get('redundancy_rate', 1.0)
        
        ga_entropy = ga_quality.get('representation_entropy', 0.0)
        trad_entropy = trad_quality.get('representation_entropy', 0.0)
        
        ga_diversity = ga_quality.get('feature_diversity_score', 0.0)
        trad_diversity = trad_quality.get('feature_diversity_score', 0.0)
        
        # Safely get execution times with defaults
        ga_time = ga_results.get('execution_time', 0)
        trad_time = traditional_results.get('execution_time', 0)
        
        # Calculate overlap safely
        common_features = list(ga_features & traditional_features)
        all_features = ga_features | traditional_features
        overlap_percentage = len(common_features) / max(len(all_features), 1) * 100
        
        # Determine winners for each metric
        redundancy_winner = "GA" if ga_redundancy < trad_redundancy else "Traditional"
        entropy_winner = "GA" if ga_entropy > trad_entropy else "Traditional"
        diversity_winner = "GA" if ga_diversity > trad_diversity else "Traditional"
        
        comparison = {
            'feature_quality_comparison': {
                'redundancy_rate': {
                    'ga': float(ga_redundancy),
                    'traditional': float(trad_redundancy),
                    'winner': redundancy_winner,
                    'improvement': float(trad_redundancy - ga_redundancy)  # Positive means GA improved
                },
                'representation_entropy': {
                    'ga': float(ga_entropy),
                    'traditional': float(trad_entropy),
                    'winner': entropy_winner,
                    'improvement': float(ga_entropy - trad_entropy)  # Positive means GA improved
                },
                'feature_diversity_score': {
                    'ga': float(ga_diversity),
                    'traditional': float(trad_diversity),
                    'winner': diversity_winner,
                    'improvement': float(ga_diversity - trad_diversity)  # Positive means GA improved
                }
            },
            'feature_count_comparison': {
                'ga': int(ga_results.get('num_features', 0)),
                'traditional': int(traditional_results.get('num_features', 0)),
                'difference': int(ga_results.get('num_features', 0) - traditional_results.get('num_features', 0)),
                'reduction_ga': ga_results.get('feature_reduction', '0.0%'),
                'reduction_traditional': traditional_results.get('feature_reduction', '0.0%')
            },
            'performance_comparison': {
                'execution_time_ga': float(ga_time),
                'execution_time_traditional': float(trad_time),
                'time_ratio': float(trad_time / max(ga_time, 0.1))  # Avoid division by zero
            },
            'feature_analysis': {
                'common_features': common_features,
                'unique_to_ga': list(ga_features - traditional_features),
                'unique_to_traditional': list(traditional_features - ga_features),
                'overlap_percentage': float(overlap_percentage)
            },
            'recommendation': generate_recommendation(ga_results, traditional_results)
        }
        
        return convert_to_serializable(comparison)
        
    except Exception as e:
        logger.error(f"Error comparing methods: {e}")
        return convert_to_serializable({
            'error': f"Comparison failed: {str(e)}",
            'feature_quality_comparison': {
                'redundancy_rate': {'ga': 1.0, 'traditional': 1.0, 'winner': 'Unknown', 'improvement': 0},
                'representation_entropy': {'ga': 0.0, 'traditional': 0.0, 'winner': 'Unknown', 'improvement': 0},
                'feature_diversity_score': {'ga': 0.0, 'traditional': 0.0, 'winner': 'Unknown', 'improvement': 0}
            },
            'feature_count_comparison': {'ga': 0, 'traditional': 0, 'difference': 0, 'reduction_ga': '0%', 'reduction_traditional': '0%'},
            'performance_comparison': {'execution_time_ga': 0, 'execution_time_traditional': 0, 'time_ratio': 0},
            'feature_analysis': {'common_features': [], 'unique_to_ga': [], 'unique_to_traditional': [], 'overlap_percentage': 0},
            'recommendation': 'Unable to generate recommendation due to error'
        })
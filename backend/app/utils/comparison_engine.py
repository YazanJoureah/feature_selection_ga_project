from typing import Dict, Any
from .serialization import convert_to_serializable


def _extract_comparison_metrics(ga_results: Dict[str, Any], traditional_results: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and calculate metrics for comparison"""
    ga_quality = ga_results.get('feature_quality', {})
    trad_quality = traditional_results.get('feature_quality', {})
    
    # Extract quality metrics
    ga_redundancy = ga_quality.get('redundancy_rate', 1.0)
    trad_redundancy = trad_quality.get('redundancy_rate', 1.0)
    ga_entropy = ga_quality.get('representation_entropy', 0.0)
    trad_entropy = trad_quality.get('representation_entropy', 0.0)
    ga_diversity = ga_quality.get('feature_diversity_score', 0.0)
    trad_diversity = trad_quality.get('feature_diversity_score', 0.0)
    
    # Extract performance metrics
    ga_time = ga_results.get('execution_time', 0)
    trad_time = traditional_results.get('execution_time', 0)
    ga_feature_count = ga_results.get('num_features', 0)
    trad_feature_count = traditional_results.get('num_features', 0)
    
    # Calculate improvements
    redundancy_improvement = trad_redundancy - ga_redundancy
    entropy_improvement = ga_entropy - trad_entropy
    diversity_improvement = ga_diversity - trad_diversity
    
    # Calculate ratios
    time_ratio = ga_time / max(trad_time, 0.1)
    feature_count_ratio = ga_feature_count / max(trad_feature_count, 1)
    
    return {
        'ga_metrics': {
            'redundancy': ga_redundancy, 'entropy': ga_entropy, 'diversity': ga_diversity,
            'time': ga_time, 'feature_count': ga_feature_count
        },
        'trad_metrics': {
            'redundancy': trad_redundancy, 'entropy': trad_entropy, 'diversity': trad_diversity,
            'time': trad_time, 'feature_count': trad_feature_count
        },
        'improvements': {
            'redundancy': redundancy_improvement, 'entropy': entropy_improvement, 
            'diversity': diversity_improvement
        },
        'ratios': {
            'time': time_ratio, 'feature_count': feature_count_ratio
        }
    }

def _generate_recommendation_from_metrics(metrics: Dict[str, Any]) -> str:
    """Generate recommendation based on extracted metrics"""
    ga_metrics = metrics['ga_metrics']
    trad_metrics = metrics['trad_metrics']
    improvements = metrics['improvements']
    ratios = metrics['ratios']
    
    improvement_threshold = 0.1
    
    # Clear winner scenario - GA better on all metrics
    if (improvements['diversity'] > improvement_threshold and 
        improvements['redundancy'] > 0 and 
        improvements['entropy'] > 0):
        
        if ratios['time'] < 3:
            return (f"GA recommended - superior feature quality: "
                   f"{improvements['diversity']:.2f} better diversity, "
                   f"{improvements['redundancy']:.2f} lower redundancy, "
                   f"{improvements['entropy']:.2f} higher entropy")
        else:
            return (f"GA has better feature quality but {ratios['time']:.1f}x slower - "
                   f"consider Traditional for time-critical applications")
    
    # Clear loser scenario - Traditional better on all metrics
    elif (improvements['diversity'] < -improvement_threshold and 
          improvements['redundancy'] < 0 and 
          improvements['entropy'] < 0):
        return "Traditional method recommended - better feature quality across all metrics"
    
    # Mixed results - weighted decision
    else:
        diversity_weight = 0.4
        redundancy_weight = 0.3
        entropy_weight = 0.2
        time_weight = 0.1
        
        feature_count_penalty = abs(1 - ratios['feature_count']) * 0.1
        
        ga_score = (
            ga_metrics['diversity'] * diversity_weight +
            (1 - ga_metrics['redundancy']) * redundancy_weight +
            ga_metrics['entropy'] * entropy_weight +
            (1 / ratios['time']) * time_weight -
            feature_count_penalty
        )
        
        trad_score = (
            trad_metrics['diversity'] * diversity_weight +
            (1 - trad_metrics['redundancy']) * redundancy_weight +
            trad_metrics['entropy'] * entropy_weight +
            1 * time_weight -
            feature_count_penalty
        )
        
        # Build recommendation reason
        reason_parts = []
        if improvements['diversity'] > 0:
            reason_parts.append(f"{improvements['diversity']:.2f} better diversity")
        if improvements['redundancy'] > 0:
            reason_parts.append(f"{improvements['redundancy']:.2f} lower redundancy")
        if improvements['entropy'] > 0:
            reason_parts.append(f"{improvements['entropy']:.2f} higher entropy")
            
        reason = " and ".join(reason_parts) if reason_parts else "better overall score"
        
        if ga_score > trad_score:
            return f"GA recommended - {reason} (score: {ga_score:.2f} vs {trad_score:.2f})"
        else:
            return f"Traditional recommended - better overall feature quality score ({trad_score:.2f} vs {ga_score:.2f})"

def compare_methods_results(ga_results: Dict[str, Any], traditional_results: Dict[str, Any]) -> Dict[str, Any]:
    """Compare GA and traditional feature selection methods"""
    try:
        # Extract feature sets
        ga_features = set(ga_results.get('selected_features', []))
        traditional_features = set(traditional_results.get('selected_features', []))
        
        # Extract all metrics
        metrics = _extract_comparison_metrics(ga_results, traditional_results)
        
        # Calculate feature overlap
        common_features = list(ga_features & traditional_features)
        all_features = ga_features | traditional_features
        overlap_percentage = len(common_features) / max(len(all_features), 1) * 100
        
        # Determine winners
        redundancy_winner = "GA" if metrics['improvements']['redundancy'] > 0 else "Traditional"
        entropy_winner = "GA" if metrics['improvements']['entropy'] > 0 else "Traditional"
        diversity_winner = "GA" if metrics['improvements']['diversity'] > 0 else "Traditional"
        
        comparison = {
            'feature_quality_comparison': {
                'redundancy_rate': {
                    'ga': float(metrics['ga_metrics']['redundancy']),
                    'traditional': float(metrics['trad_metrics']['redundancy']),
                    'winner': redundancy_winner,
                    'improvement': float(metrics['improvements']['redundancy'])
                },
                'representation_entropy': {
                    'ga': float(metrics['ga_metrics']['entropy']),
                    'traditional': float(metrics['trad_metrics']['entropy']),
                    'winner': entropy_winner,
                    'improvement': float(metrics['improvements']['entropy'])
                },
                'feature_diversity_score': {
                    'ga': float(metrics['ga_metrics']['diversity']),
                    'traditional': float(metrics['trad_metrics']['diversity']),
                    'winner': diversity_winner,
                    'improvement': float(metrics['improvements']['diversity'])
                }
            },
            'feature_count_comparison': {
                'ga': int(metrics['ga_metrics']['feature_count']),
                'traditional': int(metrics['trad_metrics']['feature_count']),
                'difference': int(metrics['ga_metrics']['feature_count'] - metrics['trad_metrics']['feature_count']),
                'reduction_ga': ga_results.get('feature_reduction', '0.0%'),
                'reduction_traditional': traditional_results.get('feature_reduction', '0.0%')
            },
            'performance_comparison': {
                'execution_time_ga': float(metrics['ga_metrics']['time']),
                'execution_time_traditional': float(metrics['trad_metrics']['time']),
                'time_ratio': float(1 / metrics['ratios']['time'])  
            },
            'feature_analysis': {
                'common_features': common_features,
                'unique_to_ga': list(ga_features - traditional_features),
                'unique_to_traditional': list(traditional_features - ga_features),
                'overlap_percentage': float(overlap_percentage)
            },
            'recommendation': _generate_recommendation_from_metrics(metrics)
        }
        
        return convert_to_serializable(comparison)
        
    except Exception as e:
        print(f"Error comparing methods: {e}")
        return _create_error_comparison(str(e))

def _create_error_comparison(error_msg: str) -> Dict[str, Any]:
    """Create error response for comparison"""
    return convert_to_serializable({
        'error': f"Comparison failed: {error_msg}",
        'feature_quality_comparison': {
            'redundancy_rate': {'ga': 1.0, 'traditional': 1.0, 'winner': 'Unknown', 'improvement': 0},
            'representation_entropy': {'ga': 0.0, 'traditional': 0.0, 'winner': 'Unknown', 'improvement': 0},
            'feature_diversity_score': {'ga': 0.0, 'traditional': 0.0, 'winner': 'Unknown', 'improvement': 0}
        },
        'feature_count_comparison': {
            'ga': 0, 'traditional': 0, 'difference': 0, 
            'reduction_ga': '0%', 'reduction_traditional': '0%'
        },
        'performance_comparison': {
            'execution_time_ga': 0, 'execution_time_traditional': 0, 'time_ratio': 0
        },
        'feature_analysis': {
            'common_features': [], 'unique_to_ga': [], 
            'unique_to_traditional': [], 'overlap_percentage': 0
        },
        'recommendation': 'Unable to generate recommendation due to error'
    })
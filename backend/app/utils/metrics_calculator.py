import numpy as np
import pandas as pd
import logging
from typing import Dict,  List


def _safe_calculate_metrics(func, X, selected_features, default_value):
    """Safe wrapper for metric calculation functions"""
    try:
        return func(X, selected_features)
    except Exception as e:
        print(f"Error in {func.__name__}: {e}")
        return default_value

def calculate_redundancy_rate(X: pd.DataFrame, selected_features: List[str]) -> float:
    """Calculate Redundancy Rate - average correlation between selected features"""
    if len(selected_features) <= 1:
        return 0.0
    
    # Calculate correlation matrix for selected features
    corr_matrix = X[selected_features].corr().abs()
    
    # Get upper triangle without diagonal
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
    upper_triangle = corr_matrix.where(mask)
    
    # Calculate average correlation (excluding diagonal)
    redundancy_rate = upper_triangle.stack().mean()
    return float(redundancy_rate) if not np.isnan(redundancy_rate) else 0.0

def calculate_representation_entropy(X: pd.DataFrame, selected_features: List[str]) -> float:
    """Calculate Representation Entropy - diversity of feature importance distribution"""
    if len(selected_features) == 0:
        return 0.0
    
    # Use variance as proxy for feature importance
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
    return entropy / max_entropy if max_entropy > 0 else 0

def calculate_feature_quality_metrics(X: pd.DataFrame, selected_features: List[str]) -> Dict[str, float]:
    """Calculate comprehensive feature quality metrics"""
    if len(selected_features) == 0:
        return {
            'redundancy_rate': 1.0,
            'representation_entropy': 0.0,
            'feature_diversity_score': 0.0
        }
    
    # Calculate metrics safely
    redundancy_rate = _safe_calculate_metrics(calculate_redundancy_rate, X, selected_features, 1.0)
    representation_entropy = _safe_calculate_metrics(calculate_representation_entropy, X, selected_features, 0.0)
    
    # Combined diversity score (lower redundancy + higher entropy = better)
    feature_diversity_score = (1 - redundancy_rate) * representation_entropy
    
    return {
        'redundancy_rate': float(redundancy_rate),
        'representation_entropy': float(representation_entropy),
        'feature_diversity_score': float(feature_diversity_score)
    }
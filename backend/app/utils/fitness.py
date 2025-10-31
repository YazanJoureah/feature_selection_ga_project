import numpy as np
import pandas as pd
import logging
from typing import List, Dict, Any

def calculate_fitness(selected_features: list, X: pd.DataFrame, y: pd.Series) -> float:
    """
    Fitness calculation
    """
    if not selected_features:
        return 0.0
    
    k = len(selected_features)
    
    # Relevance
    relevance_scores = [abs(X[feat].corr(y)) for feat in selected_features]
    relevance = np.mean(relevance_scores)
    
    # Redundancy
    redundancy = 0.0
    if k > 1:
        corr_matrix = X[selected_features].corr().abs().values
        np.fill_diagonal(corr_matrix, 0)
        redundancy = corr_matrix.sum() / (k * (k - 1))
    
    # Penalty and final score
    penalty = (k / X.shape[1]) * 0.1
    return max(0.0, relevance - redundancy - penalty)
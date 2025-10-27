import numpy as np
import pandas as pd
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def convert_metrics_to_serializable(metrics_dict):
    """Convert metrics dictionary to use native Python types"""
    if not isinstance(metrics_dict, dict):
        return metrics_dict
    
    converted = {}
    for key, value in metrics_dict.items():
        if isinstance(value, (np.integer, np.int64, np.int32)):
            converted[key] = int(value)
        elif isinstance(value, (np.floating, np.float64, np.float32)):
            converted[key] = float(value)
        elif isinstance(value, np.bool_):
            converted[key] = bool(value)
        elif isinstance(value, dict):
            converted[key] = convert_metrics_to_serializable(value)
        elif isinstance(value, list):
            converted[key] = [convert_metrics_to_serializable(item) if isinstance(item, dict) else item for item in value]
        else:
            converted[key] = value
    return converted

def calculate_fitness(selected_features: List[str], X, y) -> float:
    """
    Advanced correlation-based fitness function
    - Balances relevance and redundancy
    - Penalizes too many features
    """
    try:
        if not selected_features or len(selected_features) == 0:
            return 0.0
        
        # Convert to DataFrame if needed
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        if not isinstance(y, pd.Series):
            y = pd.Series(y)
        
        # Ensure selected features exist
        available_features = X.columns.tolist() if isinstance(X, pd.DataFrame) else list(range(X.shape[1]))
        valid_features = [f for f in selected_features if f in available_features]
        
        if not valid_features:
            return 0.0
            
        X_selected = X[valid_features] if isinstance(X, pd.DataFrame) else pd.DataFrame(X)[valid_features]
        k = len(valid_features)
        total_features = X.shape[1]
        
        # 1. Calculate relevance (correlation with target)
        relevance_scores = []
        for feature in valid_features:
            try:
                x_vals = X[feature].values if isinstance(X, pd.DataFrame) else X[:, available_features.index(feature)]
                y_vals = y.values if hasattr(y, 'values') else y
                
                # Handle constant features
                if np.std(x_vals) == 0 or np.std(y_vals) == 0:
                    continue
                    
                corr = np.abs(np.corrcoef(x_vals, y_vals)[0, 1])
                if not np.isnan(corr):
                    relevance_scores.append(float(corr))  # Convert to float
            except Exception as e:
                logger.debug(f"Could not calculate correlation for {feature}: {e}")
                continue
        
        if not relevance_scores:
            return 0.0
            
        relevance = float(np.mean(relevance_scores))  # Convert to float
        
        # 2. Calculate redundancy (correlation between features)
        redundancy = 0.0
        if k > 1:
            try:
                X_np = X_selected.values if isinstance(X_selected, pd.DataFrame) else X_selected
                corr_matrix = np.corrcoef(X_np.T)
                np.fill_diagonal(corr_matrix, 0)
                redundancy = float(np.abs(corr_matrix).sum() / (k * (k - 1)))  # Convert to float
            except Exception as e:
                logger.debug(f"Could not calculate redundancy: {e}")
                redundancy = 0.0
        
        # 3. Penalty for too many features
        feature_penalty = float((k / total_features) * 0.1)  # Convert to float
        
        # 4. Combined fitness: relevance - redundancy - penalty
        fitness = relevance - redundancy - feature_penalty
        
        return max(0.0, float(fitness))  # Convert to float
        
    except Exception as e:
        logger.warning(f"Fitness calculation failed: {e}")
        return 0.0

def calculate_feature_metrics(selected_features: List[str], X, y) -> Dict[str, Any]:
    """
    Calculate comprehensive feature metrics for analysis
    """
    try:
        if not selected_features:
            return convert_metrics_to_serializable({
                'relevance': 0.0,
                'redundancy': 0.0,
                'feature_penalty': 0.0,
                'individual_correlations': {},
                'redundancy_matrix': {},
                'num_features': 0,
                'total_features': X.shape[1] if hasattr(X, 'shape') else 0
            })
        
        # Convert to DataFrame if needed
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        if not isinstance(y, pd.Series):
            y = pd.Series(y)
        
        available_features = X.columns.tolist() if isinstance(X, pd.DataFrame) else list(range(X.shape[1]))
        valid_features = [f for f in selected_features if f in available_features]
        
        if not valid_features:
            return convert_metrics_to_serializable({
                'relevance': 0.0,
                'redundancy': 0.0,
                'feature_penalty': 0.0,
                'individual_correlations': {},
                'redundancy_matrix': {},
                'num_features': 0,
                'total_features': X.shape[1]
            })
        
        X_selected = X[valid_features] if isinstance(X, pd.DataFrame) else pd.DataFrame(X)[valid_features]
        k = len(valid_features)
        total_features = X.shape[1]
        
        # Calculate individual correlations
        individual_correlations = {}
        relevance_scores = []
        
        for feature in valid_features:
            try:
                x_vals = X[feature].values if isinstance(X, pd.DataFrame) else X[:, available_features.index(feature)]
                y_vals = y.values if hasattr(y, 'values') else y
                
                if np.std(x_vals) == 0 or np.std(y_vals) == 0:
                    individual_correlations[feature] = 0.0
                    continue
                    
                corr = np.abs(np.corrcoef(x_vals, y_vals)[0, 1])
                if not np.isnan(corr):
                    individual_correlations[feature] = float(corr)  # Convert to float
                    relevance_scores.append(float(corr))  # Convert to float
                else:
                    individual_correlations[feature] = 0.0
            except Exception as e:
                logger.debug(f"Could not calculate correlation for {feature}: {e}")
                individual_correlations[feature] = 0.0
        
        relevance = float(np.mean(relevance_scores)) if relevance_scores else 0.0  # Convert to float
        
        # Calculate redundancy matrix
        redundancy = 0.0
        redundancy_matrix = {}
        if k > 1:
            try:
                X_np = X_selected.values if isinstance(X_selected, pd.DataFrame) else X_selected
                corr_matrix = np.corrcoef(X_np.T)
                
                for i, feat1 in enumerate(valid_features):
                    for j, feat2 in enumerate(valid_features):
                        if i != j:
                            key = f"{feat1}-{feat2}"
                            redundancy_matrix[key] = float(np.abs(corr_matrix[i, j]))  # Convert to float
                
                np.fill_diagonal(corr_matrix, 0)
                redundancy = float(np.abs(corr_matrix).sum() / (k * (k - 1)))  # Convert to float
            except Exception as e:
                logger.debug(f"Could not calculate redundancy matrix: {e}")
                redundancy = 0.0
        
        feature_penalty = float((k / total_features) * 0.1)  # Convert to float
        
        metrics = {
            'relevance': relevance,
            'redundancy': redundancy,
            'feature_penalty': feature_penalty,
            'individual_correlations': individual_correlations,
            'redundancy_matrix': redundancy_matrix,
            'num_features': int(k),  # Convert to int
            'total_features': int(total_features)  # Convert to int
        }
        
        return convert_metrics_to_serializable(metrics)
        
    except Exception as e:
        logger.warning(f"Feature metrics calculation failed: {e}")
        return convert_metrics_to_serializable({
            'relevance': 0.0,
            'redundancy': 0.0,
            'feature_penalty': 0.0,
            'individual_correlations': {},
            'redundancy_matrix': {},
            'num_features': 0,
            'total_features': X.shape[1] if hasattr(X, 'shape') else 0
        })
import pandas as pd
import numpy as np
import logging
from typing import Tuple, Dict, Any

logger = logging.getLogger(__name__)

def process_uploaded_file(file_path: str, file_extension: str, target_column: str) -> Tuple[pd.DataFrame, pd.Series]:
    """Process uploaded file and extract X, y"""
    try:
        # Load dataset
        if file_extension == 'csv':
            df = pd.read_csv(file_path)
        elif file_extension == 'json':
            df = pd.read_json(file_path)
        else:
            df = pd.read_excel(file_path)
        
        # Validate target column
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found")
        
        # Extract features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Basic validation
        if len(X) < 10:
            print("Dataset has less than 10 samples")
        if len(X.columns) < 2:
            raise ValueError("Dataset must have at least 2 features")
        
        # Convert categorical target to numeric
        if y.dtype == 'object':
            y = pd.factorize(y)[0]
        
        # Clean data
        X = remove_constant_features(X)
        X, y = handle_missing_values(X, y)
        
        print(f"Dataset processed: {X.shape[0]} samples, {X.shape[1]} features")
        return X, y
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise

def remove_constant_features(X: pd.DataFrame) -> pd.DataFrame:
    """Remove constant and quasi-constant features"""
    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)
    # Remove constant features
    constant_mask = X.nunique() <= 1
    constant_features = X.columns[constant_mask]
    if constant_features.any():
        X = X.drop(columns=constant_features)
    
    # Remove quasi-constant features (99% same value)
    quasi_constant = []
    for col in X.columns:
        if X[col].dtype in ['object', 'category']:
            continue
        if (X[col].value_counts().iloc[0] / len(X)) > 0.99:
            quasi_constant.append(col)
    
    if quasi_constant:
        X = X.drop(columns=quasi_constant)
    
    return X

def handle_missing_values(X: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, pd.Series]:
    """Handle missing values in features and target"""
    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)
    if not isinstance(y, pd.Series):
        y = pd.Series(y)
    # Remove rows with missing target
    missing_target = pd.isna(y)
    if missing_target.any():
        X = X[~missing_target]
        y = y[~missing_target]
    
    if isinstance(X, pd.DataFrame):
        missing_features = X.isna().sum()
        if missing_features.any():
            # Handle missing features
            for col in X.columns:
                if X[col].isna().any():
                    if X[col].dtype in ['object', 'category']:
                        X[col] = X[col].fillna(X[col].mode()[0] if not X[col].mode().empty else 'missing')
                    else:
                        X[col] = X[col].fillna(X[col].median())
    
    return X, y

def get_dataset_stats(X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
    """Get dataset statistics"""
    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)
    if not isinstance(y, pd.Series):
        y = pd.Series(y)

    stats = {
        'samples': X.shape[0],
        'features': X.shape[1],
        'target_distribution': dict(y.value_counts()),
        'missing_values': int(X.isna().sum().sum() + y.isna().sum())
    }
    
    # Feature types
    stats['feature_types'] = {
        'numerical': len(X.select_dtypes(include=[np.number]).columns),
        'categorical': len(X.select_dtypes(include=['object', 'category']).columns)
    }
    
    # Memory usage
    try:
        stats['memory_usage_mb'] = round(X.memory_usage(deep=True).sum() / 1024 / 1024, 2)
    except:
        stats['memory_usage_mb'] = 0.0
    
    # Feature correlations
    numerical_features = X.select_dtypes(include=[np.number]).columns
    if len(numerical_features) > 0:
        try:
            correlations = X[numerical_features].corrwith(y).abs()
            stats['avg_feature_correlation'] = round(correlations.mean(), 4)
            stats['max_feature_correlation'] = round(correlations.max(), 4)
        except:
            stats['avg_feature_correlation'] = 0.0
            stats['max_feature_correlation'] = 0.0
    else:
        stats['avg_feature_correlation'] = 0.0
        stats['max_feature_correlation'] = 0.0
    
    return stats
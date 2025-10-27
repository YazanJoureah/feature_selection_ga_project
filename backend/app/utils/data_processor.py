import pandas as pd
import numpy as np
import logging
from typing import Tuple, Dict, Any

logger = logging.getLogger(__name__)

def process_uploaded_file(file_path: str, file_extension: str, target_column: str) -> Tuple[pd.DataFrame, pd.Series]:
    """Process uploaded file and extract X, y with validation"""
    try:
        logger.info(f"Processing dataset: {file_path}")
        
        # Load dataset based on file type
        if file_extension == 'csv':
            df = pd.read_csv(file_path)
        elif file_extension == 'json':
            df = pd.read_json(file_path)
        else:  # Excel files
            df = pd.read_excel(file_path)
        
        # Validate target column exists
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataset")
        
        # Extract features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Validate dataset has sufficient data
        if len(X) < 10:
            logger.warning("Dataset has less than 10 samples, proceeding anyway")
        
        if len(X.columns) < 2:
            raise ValueError("Dataset must have at least 2 features")
        
        # Convert target to numeric if categorical
        if y.dtype == 'object':
            y = pd.factorize(y)[0]
            logger.info("Converted categorical target to numeric")
        
        # Remove constant features
        X = remove_constant_features(X)
        
        # Handle missing values
        X, y = handle_missing_values(X, y)
        
        logger.info(f"Dataset processed: {X.shape[0]} samples, {X.shape[1]} features")
        
        return X, y
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise

def remove_constant_features(X: pd.DataFrame) -> pd.DataFrame:
    """Remove constant and quasi-constant features - FIXED for pandas"""
    # Make sure X is a DataFrame
    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)
    
    # Remove constant features
    constant_features = X.columns[X.nunique() <= 1]
    if len(constant_features) > 0:
        logger.info(f"Removing constant features: {list(constant_features)}")
        X = X.drop(columns=constant_features)
    
    # Remove quasi-constant features (99% same value)
    quasi_constant = []
    for col in X.columns:
        if X[col].dtype in ['object', 'category']:
            continue  # Skip categorical for this check
        most_frequent_ratio = (X[col].value_counts().iloc[0] / len(X))
        if most_frequent_ratio > 0.99:
            quasi_constant.append(col)
    
    if quasi_constant:
        logger.info(f"Removing quasi-constant features: {quasi_constant}")
        X = X.drop(columns=quasi_constant)
    
    return X

def handle_missing_values(X: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, pd.Series]:
    """Handle missing values in features and target - FIXED for pandas"""
    # Ensure we're working with pandas objects
    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)
    if not isinstance(y, pd.Series):
        y = pd.Series(y)
    
    # Remove rows with missing target
    missing_target = pd.isna(y)
    if missing_target.any():
        logger.info(f"Removing {missing_target.sum()} rows with missing target")
        X = X[~missing_target]
        y = y[~missing_target]
    
    # Handle missing features - only if X is DataFrame
    if isinstance(X, pd.DataFrame):
        missing_features = X.isna().sum()
        if missing_features.any():
            logger.info(f"Handling missing values in {len(missing_features[missing_features > 0])} features")
            
            for col in X.columns:
                if X[col].isna().any():
                    if X[col].dtype in ['object', 'category']:
                        # Categorical: fill with mode
                        X[col] = X[col].fillna(X[col].mode()[0] if not X[col].mode().empty else 'missing')
                    else:
                        # Numerical: fill with median
                        X[col] = X[col].fillna(X[col].median())
    
    return X, y

def get_dataset_stats(X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
    """Get comprehensive dataset statistics - FIXED for mixed types"""
    # Ensure we're working with pandas objects
    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)
    if not isinstance(y, pd.Series):
        y = pd.Series(y)
    
    stats = {
        'samples': X.shape[0],
        'features': X.shape[1],
        'target_distribution': dict(y.value_counts()),
        'missing_values': int(X.isna().sum().sum() + y.isna().sum()) if isinstance(X, pd.DataFrame) else 0
    }
    
    # Add feature types if X is DataFrame
    if isinstance(X, pd.DataFrame):
        stats['feature_types'] = {
            'numerical': len(X.select_dtypes(include=[np.number]).columns),
            'categorical': len(X.select_dtypes(include=['object', 'category']).columns)
        }
        
        # Add memory usage
        try:
            stats['memory_usage_mb'] = round(X.memory_usage(deep=True).sum() / 1024 / 1024, 2)
        except:
            stats['memory_usage_mb'] = 0.0
        
        # Add basic feature correlations if numerical features exist
        numerical_features = X.select_dtypes(include=[np.number]).columns
        if len(numerical_features) > 0 and len(y) > 0:
            try:
                correlations = X[numerical_features].corrwith(y).abs()
                stats['avg_feature_correlation'] = round(correlations.mean(), 4)
                stats['max_feature_correlation'] = round(correlations.max(), 4)
            except Exception as e:
                logger.warning(f"Could not calculate correlations: {e}")
                stats['avg_feature_correlation'] = 0.0
                stats['max_feature_correlation'] = 0.0
    else:
        stats['feature_types'] = {'numerical': X.shape[1], 'categorical': 0}
        stats['memory_usage_mb'] = 0.0
        stats['avg_feature_correlation'] = 0.0
        stats['max_feature_correlation'] = 0.0
    
    return stats
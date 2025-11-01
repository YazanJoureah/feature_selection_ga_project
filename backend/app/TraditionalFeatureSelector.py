import numpy as np
import pandas as pd
import logging
from sklearn.feature_selection import RFE, VarianceThreshold, SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from app.utils.results_formatter import format_selection_results

logger = logging.getLogger(__name__)

class TraditionalFeatureSelector:
    def __init__(self, n_features=None, random_state=42, method='rfe', 
                 variance_threshold=0.01):
        self.n_features = n_features
        self.random_state = random_state
        self.method = method
        self.variance_threshold = variance_threshold
        np.random.seed(random_state)
    
    def _should_exclude_feature(self, feature_name):
        """Exclude irrelevant features like ID columns"""
        exclude_patterns = ['id', 'ID', 'Id', 'patient', 'sample']
        return any(pattern in str(feature_name).lower() for pattern in exclude_patterns)
    
    def _remove_redundant_features(self, X, y, selected_features, max_correlation=0.8):
        """Remove highly correlated features from selection"""
        if len(selected_features) <= 1:
            return selected_features
        
        # Calculate correlation matrix
        corr_matrix = X[selected_features].corr().abs()
        
        # Find features to remove
        to_remove = set()
        for i in range(len(selected_features)):
            for j in range(i+1, len(selected_features)):
                if corr_matrix.iloc[i, j] > max_correlation:
                    # Remove the feature with lower correlation to target
                    feat1, feat2 = selected_features[i], selected_features[j]
                    corr1 = abs(X[feat1].corr(y))
                    corr2 = abs(X[feat2].corr(y))
                    
                    if corr1 < corr2:
                        to_remove.add(feat1)
                    else:
                        to_remove.add(feat2)
        
        # Return non-redundant features
        return [f for f in selected_features if f not in to_remove]
    
    def _select_by_correlation(self, X, y, n_features):
        """Select features based on correlation with target"""
        correlations = {}
        for feature in X.columns:
            if feature != 'id':  
                corr = abs(X[feature].corr(y))
                if not np.isnan(corr):
                    correlations[feature] = corr
        
   
        # Sort by correlation and select top n
        sorted_features = sorted(correlations.items(), key=lambda x: x[1], reverse=True)
        selected = [feature for feature, score in sorted_features[:n_features]]
        selected = [f for f in selected if not self._should_exclude_feature(f)]
        
        # Remove redundant features
        return self._remove_redundant_features(X, y, selected)
    
    def _select_by_variance(self, X, y, n_features):
        """Select features based on variance threshold"""
        try:
            # First, remove low variance features
            selector = VarianceThreshold(threshold=self.variance_threshold)
            selector.fit_transform(X)
            selected_features = X.columns[selector.get_support()].tolist()
            selected_features = [f for f in selected_features if not self._should_exclude_feature(f)]
            
            print(f"Variance threshold selected {len(selected_features)} features")
            
            if len(selected_features) == 0:
                # Fallback if no features pass variance threshold
                print("No features passed variance threshold, using correlation method")
                selected_features = self._select_by_correlation(X, y, n_features)
            
            return selected_features
            
        except Exception as e:
            print(f"Variance selection failed: {e}, using correlation fallback")
            return self._select_by_correlation(X, y, n_features)
    
    def _select_by_kbest(self, X, y, n_features):
        """Select features using SelectKBest"""
        try:
            selector = SelectKBest(score_func=f_classif, k=n_features)
            selector.fit_transform(X, y)  
            selected_features = X.columns[selector.get_support()].tolist()
            selected_features = [f for f in selected_features if not self._should_exclude_feature(f)]
            
            return selected_features
            
        except Exception as e:
            print(f"SelectKBest failed: {e}, using correlation fallback")
            return self._select_by_correlation(X, y, n_features)
    
    def run(self, X, y):
        """Run traditional feature selection with multiple methods"""
        print(f"Starting Traditional Feature Selection with method: {self.method}")
        
        n_features = X.shape[1]
        
        # Determine optimal number of features if not specified
        if self.n_features is None:
            self.n_features = max(1, min(10, n_features // 3))
        
        try:
            if self.method == 'correlation':
                selected_features = self._select_by_correlation(X, y, self.n_features)
                
            elif self.method == 'variance':
                selected_features = self._select_by_variance(X, y, self.n_features)
                
            elif self.method == 'kbest':
                selected_features = self._select_by_kbest(X, y, self.n_features)
                
            else:  # RFE Recursive Feature Elimination (default)
                estimator = RandomForestClassifier(
                    n_estimators=100,
                    random_state=self.random_state
                )
                
                rfe = RFE(
                    estimator=estimator, 
                    n_features_to_select=self.n_features
                )
                
                rfe.fit(X, y)
                selected_features = X.columns[rfe.support_].tolist()
            
            # Format results
            results = format_selection_results(
                method=f'Traditional ({self.method.upper()})',
                selected_features=selected_features,
                X=X,
                additional_params={
                    'n_features': self.n_features,
                    'random_state': self.random_state,
                    'method': self.method,
                    'variance_threshold': self.variance_threshold if self.method == 'variance' else None,
                }
            )
            
            print(f"Traditional Selection Completed! Selected {len(selected_features)} features")
            print(f"   Method: {self.method}")
            
            return results
            
        except Exception as e:
            print(f"Traditional feature selection failed: {e}")
            # Fallback to correlation method
            selected_features = self._select_by_correlation(X, y, self.n_features)
            return format_selection_results(
                method='Traditional (Correlation)',
                selected_features=selected_features,
                X=X,
            )
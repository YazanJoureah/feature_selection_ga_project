import numpy as np
import pandas as pd
import logging
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from app.utils.fitness import calculate_fitness
from app.utils.results_formatter import format_selection_results

logger = logging.getLogger(__name__)

class TraditionalFeatureSelector:
    def __init__(self, n_features=None, random_state=42, method='rfe'):
        self.n_features = n_features
        self.random_state = random_state
        self.method = method
        np.random.seed(random_state)
    
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
            # Exclude ID column
            if feature != 'id':  
                corr = abs(X[feature].corr(y))
                if not np.isnan(corr):
                    correlations[feature] = corr
        
        # Sort by correlation and select top n
        sorted_features = sorted(correlations.items(), key=lambda x: x[1], reverse=True)
        selected = [feature for feature, score in sorted_features[:n_features]]
        
        # Remove redundant features
        return self._remove_redundant_features(X, y, selected)
    
    def run(self, X, y):
        """Run traditional feature selection"""
        logger.info("Starting Traditional Feature Selection...")
        
        n_features = X.shape[1]
        
        # Determine optimal number of features if not specified
        if self.n_features is None:
            self.n_features = max(1, min(10, n_features // 3))
        
        try:
            if self.method == 'correlation':
                # Use correlation-based selection
                selected_features = self._select_by_correlation(X, y, self.n_features)
            else:
                # Use Recursive Feature Elimination with better estimator
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
                
                # If RFE selects poor features, fall back to correlation
                fitness = calculate_fitness(selected_features, X, y)
                if fitness < 0.1:  # If fitness is too low
                    logger.info("RFE selected poor features, using correlation fallback")
                    selected_features = self._select_by_correlation(X, y, self.n_features)
            
            # Format results
            results = format_selection_results(
                method=f'Traditional ({self.method.upper()})',
                selected_features=selected_features,
                X=X,
                y=y,
                additional_params={
                    'n_features': self.n_features,
                    'random_state': self.random_state,
                    'method': self.method
                }
            )
            
            logger.info(f"Traditional Selection Completed! Selected {len(selected_features)} features")
            logger.info(f"   Fitness: {results['fitness_score']:.4f}")
            
            return results
            
        except Exception as e:
            logger.error(f"Traditional feature selection failed: {e}")
            # Fallback to correlation method
            selected_features = self._select_by_correlation(X, y, self.n_features)
            return format_selection_results(
                method='Traditional (Correlation)',
                selected_features=selected_features,
                X=X,
                y=y
            )
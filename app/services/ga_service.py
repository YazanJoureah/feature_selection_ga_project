import pandas as pd
import time
import logging
from app.ga_feature_selection import GeneticFeatureSelector

logger = logging.getLogger(__name__)

def run_genetic_algorithm(X, y, ga_params=None):
    """Run Genetic Algorithm feature selection"""
    logger.info("🧬 Starting Genetic Algorithm Feature Selection...")
    
    # Default GA parameters
    default_params = {
        'population_size': 30,
        'generations': 50,
        'crossover_prob': 0.8,
        'mutation_prob': 0.1,
        'random_state': 42
    }
    
    # Update with any provided parameters
    if ga_params:
        default_params.update(ga_params)
    
    start_time = time.time()
    
    try:
        # Initialize and run GA
        selector = GeneticFeatureSelector(**default_params)
        results = selector.run(X, y)
        
        execution_time = time.time() - start_time
        results['execution_time'] = round(execution_time, 2)
        
        logger.info(f"✅ GA Completed in {execution_time:.2f}s")
        logger.info(f"   Selected {results['num_features']} features")
        logger.info(f"   Fitness Score: {results['fitness_score']:.4f}")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ GA failed: {e}")
        raise

def process_uploaded_file(file_path, file_extension, target_column):
    """Process uploaded file and extract X, y"""
    try:
        logger.info(f"📊 Processing dataset: {file_path}")
        
        # Load dataset based on file type
        if file_extension == 'csv':
            df = pd.read_csv(file_path)
        elif file_extension == 'json':
            df = pd.read_json(file_path)
        else:  # Excel files
            df = pd.read_excel(file_path)
        
        # Extract features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Convert target to numeric if categorical
        if y.dtype == 'object':
            y = pd.factorize(y)[0]
            logger.info("🔄 Converted categorical target to numeric")
        
        logger.info(f"✅ Dataset processed: {X.shape[0]} samples, {X.shape[1]} features")
        
        return X, y
        
    except Exception as e:
        logger.error(f"❌ Error processing file: {str(e)}")
        raise
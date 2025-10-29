from flask_restful import Resource, reqparse
from flask import request, current_app
import os
import uuid
import logging
import numpy as np
from app.utils.validators import validate_file, validate_dataset_content
from app.utils.error_handlers import APIError
from app.utils.data_processor import process_uploaded_file, get_dataset_stats
from app.services.ga_service import run_genetic_algorithm
from app.services.traditional_service import run_traditional_method
from app.utils.results_formatter import compare_methods_results

logger = logging.getLogger(__name__)

def ensure_serializable(data):
    """Ensure all data is JSON serializable"""
    if isinstance(data, (np.integer, np.int64, np.int32)):
        return int(data)
    elif isinstance(data, (np.floating, np.float64, np.float32)):
        return float(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, np.bool_):
        return bool(data)
    elif isinstance(data, dict):
        return {key: ensure_serializable(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [ensure_serializable(item) for item in data]
    else:
        return data

class FeatureSelectionAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        # Required parameters
        parser.add_argument('target_column', type=str, required=True, location='form')
        parser.add_argument('method', type=str, default='ga', 
                          choices=['ga', 'traditional'], location='form')
        
        # GA-specific parameters
        parser.add_argument('population_size', type=int, default=30, location='form')
        parser.add_argument('generations', type=int, default=50, location='form')
        parser.add_argument('crossover_prob', type=float, default=0.8, location='form')
        parser.add_argument('mutation_prob', type=float, default=0.1, location='form')
        
        # Traditional method parameters
        parser.add_argument('n_features', type=int, default=None, location='form')
        parser.add_argument('random_state', type=int, default=42, location='form')
        parser.add_argument('traditional_method', type=str, default='rfe', 
                          choices=['rfe', 'correlation', 'variance', 'kbest'], location='form')
        parser.add_argument('variance_threshold', type=float, default=0.01, location='form')
        
        # Additional options
        parser.add_argument('run_both', type=bool, default=False, location='form')
        
        args = parser.parse_args()
        
        if 'file' not in request.files:
            return {'success': False, 'error': 'No file provided'}, 400
        
        file = request.files['file']
        file_path = None
        
        try:
            # 1. Validate file
            file_extension = validate_file(file)
            
            # 2. Save file with unique name
            filename = f"{uuid.uuid4()}_{file.filename}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # 3. Validate dataset content
            df = validate_dataset_content(file_path, file_extension, args['target_column'])
            
            # 4. Process dataset
            X, y = process_uploaded_file(file_path, file_extension, args['target_column'])
            
            # 5. Get dataset statistics
            dataset_stats = get_dataset_stats(X, y)
            
            # 6. Run feature selection based on method
            if args['run_both']:
                results = self._run_both_methods(X, y, args)
                method_name = "Both (GA and Traditional)"
            elif args['method'] == 'ga':
                results = self._run_ga_method(X, y, args)
                method_name = "Genetic Algorithm"
            else:
                results = self._run_traditional_method(X, y, args)
                method_name = f"Traditional ({args['traditional_method'].upper()})"
            
            # 7. Return success response
            response_data = {
                'success': True,
                'message': f"Feature selection completed successfully using {method_name}",
                'method_used': method_name,
                'dataset_info': {
                    'samples': X.shape[0],
                    'features': X.shape[1],
                    'target_column': args['target_column'],
                    'stats': dataset_stats
                },
                'results': results
            }
            
            return ensure_serializable(response_data), 200
            
        except APIError as e:
            self._cleanup_file(file_path)
            return {'success': False, 'error': str(e)}, 400
        except Exception as e:
            self._cleanup_file(file_path)
            logger.error(f"Feature selection failed: {str(e)}", exc_info=True)
            return ensure_serializable({
                'success': False, 
                'error': f"Feature selection failed: {str(e)}"
            }), 500

    def _run_ga_method(self, X, y, args):
        """Run Genetic Algorithm feature selection"""
        ga_params = {
            'population_size': args['population_size'],
            'generations': args['generations'],
            'crossover_prob': args['crossover_prob'],
            'mutation_prob': args['mutation_prob'],
            'random_state': args['random_state']
        }
        return run_genetic_algorithm(X, y, ga_params)

    def _run_traditional_method(self, X, y, args):
        """Run Traditional feature selection with method selection"""
        traditional_params = {
            'n_features': args['n_features'],
            'random_state': args['random_state'],
            'method': args['traditional_method'],
            'variance_threshold': args['variance_threshold']
        }
        return run_traditional_method(X, y, traditional_params)

    def _run_both_methods(self, X, y, args):
        """Run both methods and return comparison"""
        ga_results = self._run_ga_method(X, y, args)
        traditional_results = self._run_traditional_method(X, y, args)
        comparison = compare_methods_results(ga_results, traditional_results)
        
        return {
            'ga_results': ga_results,
            'traditional_results': traditional_results,
            'comparison': comparison
        }

    def _cleanup_file(self, file_path):
        """Clean up uploaded file"""
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up file {file_path}: {e}")

class FeatureSelectionComparisonAPI(Resource):
    """API for comparing multiple feature selection runs"""
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('target_column', type=str, required=True, location='form')
        parser.add_argument('methods', type=str, action='append', required=True, 
                          choices=['ga', 'traditional'], location='form')
        parser.add_argument('random_state', type=int, default=42, location='form')
        
        # Add traditional method parameters for consistency
        parser.add_argument('traditional_method', type=str, default='rfe', 
                          choices=['rfe', 'correlation', 'variance', 'kbest'], location='form')
        parser.add_argument('n_features', type=int, default=None, location='form')
        parser.add_argument('variance_threshold', type=float, default=0.01, location='form')
        
        # Add GA parameters for consistency
        parser.add_argument('population_size', type=int, default=30, location='form')
        parser.add_argument('generations', type=int, default=50, location='form')
        parser.add_argument('crossover_prob', type=float, default=0.8, location='form')
        parser.add_argument('mutation_prob', type=float, default=0.1, location='form')
        
        args = parser.parse_args()
        
        if 'file' not in request.files:
            return {'success': False, 'error': 'No file provided'}, 400
        
        file = request.files['file']
        file_path = None
        
        try:
            # Validate and process file
            file_extension = validate_file(file)
            filename = f"{uuid.uuid4()}_{file.filename}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            df = validate_dataset_content(file_path, file_extension, args['target_column'])
            X, y = process_uploaded_file(file_path, file_extension, args['target_column'])
            dataset_stats = get_dataset_stats(X, y)
            
            # Run selected methods with full parameters
            results = {}
            for method in args['methods']:
                if method == 'ga':
                    ga_params = {
                        'population_size': args['population_size'],
                        'generations': args['generations'],
                        'crossover_prob': args['crossover_prob'],
                        'mutation_prob': args['mutation_prob'],
                        'random_state': args['random_state']
                    }
                    results['ga'] = run_genetic_algorithm(X, y, ga_params)
                else:
                    traditional_params = {
                        'n_features': args['n_features'],
                        'random_state': args['random_state'],
                        'method': args['traditional_method'],
                        'variance_threshold': args['variance_threshold']
                    }
                    results['traditional'] = run_traditional_method(X, y, traditional_params)
            
            # Add comparison if both methods were run
            comparison = None
            if 'ga' in results and 'traditional' in results:
                comparison = compare_methods_results(results['ga'], results['traditional'])
            
            response_data = {
                'success': True,
                'message': f"Comparison completed for methods: {', '.join(args['methods'])}",
                'dataset_info': {
                    'samples': X.shape[0],
                    'features': X.shape[1],
                    'target_column': args['target_column'],
                    'stats': dataset_stats
                },
                'results': results,
                'comparison': comparison
            }
            
            return ensure_serializable(response_data), 200
            
        except APIError as e:
            self._cleanup_file(file_path)
            return {'success': False, 'error': str(e)}, 400
        except Exception as e:
            self._cleanup_file(file_path)
            logger.error(f"Comparison failed: {str(e)}", exc_info=True)
            return ensure_serializable({
                'success': False, 
                'error': f"Comparison failed: {str(e)}"
            }), 500

    def _cleanup_file(self, file_path):
        """Clean up uploaded file"""
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up file {file_path}: {e}")
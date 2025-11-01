from flask_restful import Resource
from flask import request
from app.services.ga_service import run_genetic_algorithm
from app.services.traditional_service import run_traditional_method
from app.utils.comparison_engine import compare_methods_results
from app.utils.error_handlers import APIError
from .base import BaseFeatureSelection


class FeatureSelectionComparisonAPI(Resource, BaseFeatureSelection):
    """API for comparing multiple feature selection runs"""
    
    def post(self):
        # Setup parser with comparison API specific arguments
        parser = self._setup_common_parser()
        parser.add_argument('methods', type=str, action='append', required=True, 
                          choices=['ga', 'traditional'], location='form')
        
        args = parser.parse_args()
        
        if 'file' not in request.files:
            raise APIError("No file provided", status_code=400)
        
        file = request.files['file']
        file_path = None
        
        try:
            # Process uploaded file
            X, y, dataset_stats, file_path = self._process_uploaded_file(
                file, args['target_column']
            )
            
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
            
            return self._create_success_response(
                X, args['target_column'], dataset_stats, 
                f"Comparison ({', '.join(args['methods'])})", 
                response_data
            )
            
        except APIError as e:
            return self._create_error_response(file_path, e, e.status_code)
        except Exception as e:
            return self._create_error_response(file_path, e, 500)
from flask_restful import Resource
from flask import request
from app.services.ga_service import run_genetic_algorithm
from app.services.traditional_service import run_traditional_method
from app.utils.comparison_engine import compare_methods_results
from app.utils.error_handlers import APIError
from .base import BaseFeatureSelection


class FeatureSelectionAPI(Resource, BaseFeatureSelection):
    def post(self):
        # Setup parser with individual API specific arguments
        parser = self._setup_common_parser()
        parser.add_argument('method', type=str, default='ga', 
                          choices=['ga', 'traditional'], location='form')
        parser.add_argument('run_both', type=bool, default=False, location='form')
        
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
            
            # Run feature selection based on method
            if args['run_both']:
                results = self._run_both_methods(X, y, args)
                method_name = "Both (GA and Traditional)"
            elif args['method'] == 'ga':
                results = self._run_ga_method(X, y, args)
                method_name = "Genetic Algorithm"
            else:
                results = self._run_traditional_method(X, y, args)
                method_name = f"Traditional ({args['traditional_method'].upper()})"
            
            return self._create_success_response(
                X, args['target_column'], dataset_stats, method_name, results
            )
            
        except APIError as e:
            return self._create_error_response(file_path, e, e.status_code)
        except Exception as e:
            return self._create_error_response(file_path, e, 500)

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
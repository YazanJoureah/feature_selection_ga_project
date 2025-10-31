import os
import uuid
from flask_restful import reqparse
from flask import current_app
from app.utils.validators import validate_file, validate_dataset_content
from app.utils.error_handlers import APIError
from app.utils.data_processor import process_uploaded_file, get_dataset_stats
from app.utils.serialization import convert_to_serializable


class BaseFeatureSelection:
    """Base class with common functionality for feature selection APIs"""
    
    def _setup_common_parser(self):
        """Setup common parser arguments for both APIs"""
        parser = reqparse.RequestParser()
        
        # Required parameters
        parser.add_argument('target_column', type=str, required=True, location='form')
        parser.add_argument('random_state', type=int, default=42, location='form')
        
        # GA parameters
        parser.add_argument('population_size', type=int, default=30, location='form')
        parser.add_argument('generations', type=int, default=50, location='form')
        parser.add_argument('crossover_prob', type=float, default=0.8, location='form')
        parser.add_argument('mutation_prob', type=float, default=0.1, location='form')
        
        # Traditional method parameters
        parser.add_argument('n_features', type=int, default=None, location='form')
        parser.add_argument('traditional_method', type=str, default='rfe', 
                          choices=['rfe', 'correlation', 'variance', 'kbest'], location='form')
        parser.add_argument('variance_threshold', type=float, default=0.01, location='form')
        
        return parser
    
    def _process_uploaded_file(self, file, target_column):
        """Common file processing logic"""
        # Validate file
        file_extension = validate_file(file)
        
        # Save file with unique name
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Validate dataset content
        df = validate_dataset_content(file_path, file_extension, target_column)
        
        # Process dataset
        X, y = process_uploaded_file(file_path, file_extension, target_column)
        
        # Get dataset statistics
        dataset_stats = get_dataset_stats(X, y)
        
        return X, y, dataset_stats, file_path
    
    def _cleanup_file(self, file_path):
        """Clean up uploaded file"""
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Cleaned up file: {file_path}")
            except Exception as e:
                print(f"Failed to clean up file {file_path}: {e}")
    
    def _create_success_response(self, X, target_column, dataset_stats, method_name, results):
        """Create standardized success response"""
        response_data = {
            'success': True,
            'message': f"Feature selection completed successfully using {method_name}",
            'method_used': method_name,
            'dataset_info': {
                'samples': X.shape[0],
                'features': X.shape[1],
                'target_column': target_column,
                'stats': dataset_stats
            },
            'results': results
        }
        
        return convert_to_serializable(response_data), 200
    
    def _create_error_response(self, file_path, error, status_code=500):
        """Create standardized error response - UPDATED for enhanced APIError"""
        self._cleanup_file(file_path)
        
        if status_code == 400:
            # Handle APIError with details
            if hasattr(error, 'details') and error.details:
                return {
                    'success': False, 
                    'error': error.message,
                    'details': error.details
                }, 400
            else:
                return {'success': False, 'error': str(error)}, 400
        else:
            print(f"Feature selection failed: {str(error)}")
            return convert_to_serializable({
                'success': False, 
                'error': f"Feature selection failed: {str(error)}"
            }), 500
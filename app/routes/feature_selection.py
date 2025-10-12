from flask_restful import Resource, reqparse
from flask import request, current_app
import os
import uuid
from app.utils.validators import validate_file, validate_dataset_content
from app.utils.error_handlers import APIError
from app.services.ga_service import run_genetic_algorithm, process_uploaded_file

class FeatureSelectionAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('target_column', type=str, required=True, location='form')
        parser.add_argument('population_size', type=int, default=30, location='form')
        parser.add_argument('generations', type=int, default=50, location='form')
        parser.add_argument('crossover_prob', type=float, default=0.8, location='form')
        parser.add_argument('mutation_prob', type=float, default=0.1, location='form')
        
        args = parser.parse_args()
        
        if 'file' not in request.files:
            return {'success': False, 'error': 'No file provided'}, 400
        
        file = request.files['file']
        
        # Store file path for cleanup
        file_path = None
        
        try:
            # 1. Validate file
            file_extension = validate_file(file)
            
            # 2. Save file with unique name
            filename = f"{uuid.uuid4()}_{file.filename}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # 3. Validate dataset content (now returns only DataFrame)
            df = validate_dataset_content(file_path, file_extension, args['target_column'])
            
            # 4. Process dataset using the service
            X, y = process_uploaded_file(file_path, file_extension, args['target_column'])
            
            # 5. Prepare GA parameters
            ga_params = {
                'population_size': args['population_size'],
                'generations': args['generations'],
                'crossover_prob': args['crossover_prob'],
                'mutation_prob': args['mutation_prob']
            }
            
            # 6. Run Genetic Algorithm
            results = run_genetic_algorithm(X, y, ga_params)
            
            # 7. Return success response
            return {
                'success': True,
                'message': "Feature selection completed successfully",
                'dataset_info': {
                    'samples': X.shape[0],
                    'features': X.shape[1],
                    'target_column': args['target_column']
                },
                'results': results
            }, 200
            
        except APIError as e:
            # Clean up file if there was an error
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass
            return {'success': False, 'error': str(e)}, 400
            
        except Exception as e:
            # Clean up file if there was an error
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass
            return {'success': False, 'error': f"Feature selection failed: {str(e)}"}, 500
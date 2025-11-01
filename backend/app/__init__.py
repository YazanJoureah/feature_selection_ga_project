from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # Basic configuration
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
    app.config['JSON_SORT_KEYS'] = False
    
    # Initialize extensions
    api = Api(app)
    CORS(app)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Register routes
    from app.routes.feature_selection import FeatureSelectionAPI, FeatureSelectionComparisonAPI
    api.add_resource(FeatureSelectionAPI, '/api/feature-selection')
    api.add_resource(FeatureSelectionComparisonAPI, '/api/feature-selection/compare')
    
    return app
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os

def create_app(config_class='config.DevelopmentConfig'):
    """
    Application factory pattern
    Creates and configures the Flask application
    """
    app = Flask(__name__)
    
    # Load configuration from class
    app.config.from_object(config_class)
    
    # Initialize extensions
    api = Api(app)
    CORS(app)  # Enable CORS for all routes
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Import and register routes from routes package
    from app.routes.feature_selection import FeatureSelectionAPI, FeatureSelectionComparisonAPI
    api.add_resource(FeatureSelectionAPI, '/api/feature-selection')
    api.add_resource(FeatureSelectionComparisonAPI, '/api/feature-selection/compare')
    
    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    return app
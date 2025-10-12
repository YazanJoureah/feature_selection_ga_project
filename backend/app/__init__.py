from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object('config.DevelopmentConfig')
    
    # Initialize extensions
    api = Api(app)
    cors = CORS(app)
    
    # Create upload directory
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Register routes
    from app.routes.feature_selection import FeatureSelectionAPI
    api.add_resource(FeatureSelectionAPI, '/api/feature-selection/ga')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Feature Selection API is running'}
    
    return app
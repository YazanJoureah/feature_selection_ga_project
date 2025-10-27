from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Custom API exception"""
    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code

def register_error_handlers(app):
    """Register custom error handlers for the application"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle custom API errors"""
        logger.warning(f"API Error: {error.message}")
        return jsonify({
            'success': False,
            'error': error.message
        }), error.status_code
    
    @app.errorhandler(413)
    def handle_file_too_large(error):
        """Handle file too large errors"""
        logger.warning("File upload too large")
        return jsonify({
            'success': False,
            'error': 'File size exceeds maximum allowed limit'
        }), 413
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'success': False,
            'error': 'Resource not found'
        }), 404
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle 500 errors"""
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_generic_error(error):
        """Handle any unhandled exceptions"""
        logger.error(f"Unhandled exception: {str(error)}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred'
        }), 500
from flask import jsonify, request
import logging
import traceback

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Custom API exception"""
    def __init__(self, message, status_code=400, details=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.details = details

def register_error_handlers(app):
    """Register custom error handlers for the application"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle custom API errors"""
        logger.warning(f"API Error: {error.message} (Status: {error.status_code})")
        
        response = {
            'success': False,
            'error': error.message
        }
        
        # Add details if provided (useful for validation errors)
        if error.details:
            response['details'] = error.details
            
        return jsonify(response), error.status_code
    
    @app.errorhandler(413)
    def handle_file_too_large(error):
        """Handle file too large errors"""
        logger.warning("File upload too large")
        return jsonify({
            'success': False,
            'error': 'File size exceeds maximum allowed limit (50MB)'
        }), 413
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'success': False,
            'error': 'Resource not found',
            'path': request.path
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handle 405 Method Not Allowed errors"""
        return jsonify({
            'success': False,
            'error': 'Method not allowed for this endpoint'
        }), 405
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle 500 errors"""
        # Log full error with traceback for debugging
        logger.error(f"Internal server error: {str(error)}")
        logger.error(traceback.format_exc())
        
        # In production, don't expose internal error details
        error_message = 'Internal server error'
        if app.debug:
            error_message = f"Internal server error: {str(error)}"
            
        return jsonify({
            'success': False,
            'error': error_message
        }), 500
    
    @app.errorhandler(Exception)
    def handle_generic_error(error):
        """Handle any unhandled exceptions"""
        logger.error(f"Unhandled exception: {str(error)}")
        logger.error(traceback.format_exc())
        
        # In production, show generic message
        error_message = 'An unexpected error occurred'
        if app.debug:
            error_message = f"An unexpected error occurred: {str(error)}"
            
        return jsonify({
            'success': False,
            'error': error_message
        }), 500
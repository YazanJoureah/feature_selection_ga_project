from flask import jsonify
import traceback
import logging

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Custom API Exception"""
    def __init__(self, message, status_code=400, error_code=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

    def to_dict(self):
        return {
            'success': False,
            'error': {
                'code': self.error_code or self.status_code,
                'message': self.message
            }
        }

def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': {
                'code': 404,
                'message': 'Resource not found'
            }
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': {
                'code': 405,
                'message': 'Method not allowed'
            }
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"Internal Server Error: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': {
                'code': 500,
                'message': 'Internal server error'
            }
        }), 500

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            'success': False,
            'error': {
                'code': 413,
                'message': 'File too large'
            }
        }), 413
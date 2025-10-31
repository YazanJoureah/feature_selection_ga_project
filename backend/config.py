import os

class Config:
    """Application configuration"""
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # File handling
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # API settings
    JSON_SORT_KEYS = False
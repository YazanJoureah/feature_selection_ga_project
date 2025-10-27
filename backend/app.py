from app import create_app
import os

def get_config_class():
    """Determine configuration class based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    
    config_mapping = {
        'development': 'config.DevelopmentConfig',
        'production': 'config.ProductionConfig',
        'testing': 'config.TestingConfig'
    }
    
    return config_mapping.get(env, 'config.DevelopmentConfig')

# Create application with environment-specific configuration
app = create_app(config_class=get_config_class())

if __name__ == '__main__':
    # Run the application
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    )
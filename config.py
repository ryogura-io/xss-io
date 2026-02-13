import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///xss_prevention.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Feature Toggles
    ENABLE_DETECTION = True
    ENABLE_DASHBOARD = True

    # Content Security Policy
    CSP_POLICY = {
        'default-src': '\'self\'',
        'script-src': '\'self\'',
        'style-src': '\'self\'',
        'img-src': '\'self\' data:',
        'font-src': '\'self\'',
        'object-src': '\'none\'',
        'base-uri': '\'self\'',
        'form-action': '\'self\'',
        'frame-ancestors': '\'none\''
    }

    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

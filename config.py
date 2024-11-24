"""
Configuration settings for the Image Storage Application.

This module contains all the configuration settings for the application, including:
- Security settings
- Database configuration
- File upload settings
- Pagination settings
"""

import os

class Config:
    """
    Configuration class containing all application settings.
    
    Attributes:
        SECRET_KEY (str): Key for session security and CSRF protection
        SQLALCHEMY_DATABASE_URI (str): Database connection string
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): SQLAlchemy event tracking flag
        UPLOAD_FOLDER (str): Path where uploaded images are stored
        MAX_CONTENT_LENGTH (int): Maximum allowed file size (16MB)
        ALLOWED_EXTENSIONS (set): Allowed image file extensions
        IMAGES_PER_PAGE (int): Number of images to display per page
    """
    # Secret key for form protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-hard-to-guess-secret-key'
    
    # Database Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload Configuration
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}

    # Pagination
    IMAGES_PER_PAGE = 12

"""
Application Factory Module for the Image Storage Application.

This module contains the application factory function that creates and configures
the Flask application. It handles:
- Database initialization
- Blueprint registration
- Upload directory creation
- Initial data seeding
"""

from flask import Flask
from config import Config
from app.models import db

def create_app(config_class=Config):
    """
    Create and configure a Flask application instance.
    
    This factory function creates a new Flask application instance with the
    specified configuration. It initializes all necessary components including:
    - Database connection
    - Upload directory
    - Blueprint routes
    - Default categories and subcategories
    
    Args:
        config_class: Configuration class to use (defaults to Config)
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database
    db.init_app(app)

    # Create upload directory if it doesn't exist
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Seed initial categories and subcategories if not exists
        from app.models import Category, Subcategory
        
        # Check and create default categories if they don't exist
        default_categories = [
            'Personal', 'Work', 'Art', 'Photography', 'Design'
        ]
        
        for cat_name in default_categories:
            existing_cat = Category.query.filter_by(name=cat_name).first()
            if not existing_cat:
                new_cat = Category(name=cat_name)
                db.session.add(new_cat)
                
                # Add some default subcategories for each category
                if cat_name == 'Personal':
                    subcats = ['Family', 'Friends', 'Events', 'Travel']
                elif cat_name == 'Work':
                    subcats = ['Projects', 'Meetings', 'Documents', 'Screenshots']
                elif cat_name == 'Art':
                    subcats = ['Digital', 'Traditional', 'Sketches', 'Paintings']
                elif cat_name == 'Photography':
                    subcats = ['Landscape', 'Portrait', 'Street', 'Nature']
                else:  # Design
                    subcats = ['UI/UX', 'Graphics', 'Logos', 'Mockups']
                
                for subcat_name in subcats:
                    new_subcat = Subcategory(name=subcat_name, parent_category=new_cat)
                    db.session.add(new_subcat)
        
        db.session.commit()

    return app

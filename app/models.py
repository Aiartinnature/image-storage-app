"""
Database models for the Image Storage Application.

This module defines the SQLAlchemy models that represent the database structure:
- Category: Represents main image categories
- Subcategory: Represents subcategories within main categories
- Image: Represents stored images and their metadata
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()

class Category(db.Model):
    """
    Category model representing main image categories.
    
    Attributes:
        id (int): Primary key
        name (str): Unique category name
        subcategories (relationship): One-to-many relationship with Subcategory
        images (relationship): One-to-many relationship with Image
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    subcategories = db.relationship('Subcategory', backref='parent_category', lazy='dynamic', order_by='Subcategory.name')
    images = db.relationship('Image', backref='category', lazy=True)

class Subcategory(db.Model):
    """
    Subcategory model representing subdivisions within categories.
    
    Attributes:
        id (int): Primary key
        name (str): Subcategory name
        category_id (int): Foreign key to parent Category
        images (relationship): One-to-many relationship with Image
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    images = db.relationship('Image', backref='subcategory', lazy=True)

class Image(db.Model):
    """
    Image model representing stored images and their metadata.
    
    Attributes:
        id (int): Primary key
        name (str): Image display name
        filename (str): Actual filename on disk
        description (str): Optional image description
        prompt (str): Optional AI prompt used to generate the image
        upload_date (datetime): When the image was uploaded
        category_id (int): Foreign key to Category
        subcategory_id (int): Foreign key to Subcategory
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    prompt = db.Column(db.Text)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)

    def get_filepath(self):
        """
        Return the full file path for the image.
        
        Returns:
            str: Path to the image file relative to the application root
        """
        return os.path.join('static', 'uploads', self.filename)

    def delete_file(self):
        """
        Delete the image file from the filesystem.
        
        This method removes the actual image file from disk when an Image record
        is deleted from the database.
        """
        filepath = self.get_filepath()
        if os.path.exists(filepath):
            os.remove(filepath)

    def __repr__(self):
        """String representation of the Image model."""
        return f'<Image {self.name}>'

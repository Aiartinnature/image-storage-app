from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
import os
from flask import current_app
from werkzeug.utils import secure_filename
from .models import Image

def validate_unique_file(form, field):
    if field.data:
        filename = secure_filename(field.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Check filesystem
        if os.path.exists(filepath):
            raise ValidationError('A file with this name already exists. Please rename your file.')
        
        # Check database
        if Image.query.filter_by(filename=filename).first():
            raise ValidationError('This image has already been uploaded. Please choose a different file.')

class ImageUploadForm(FlaskForm):
    name = StringField('Image Name', validators=[
        DataRequired(), 
        Length(min=3, max=200, message='Name must be between 3 and 200 characters')
    ])
    description = TextAreaField('Description', validators=[
        Length(max=1000, message='Description cannot exceed 1000 characters')
    ])
    prompt = TextAreaField('Image Prompt', validators=[
        Length(max=500, message='Prompt cannot exceed 500 characters')
    ])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    subcategory = SelectField('Subcategory', coerce=int, validators=[DataRequired()])
    image = FileField('Upload Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp', 'svg'], 
                    'Only image files (jpg, png, jpeg, gif, webp, svg) are allowed!'),
        validate_unique_file
    ])
    submit = SubmitField('Upload Image')

class ImageEditForm(FlaskForm):
    name = StringField('Image Name', validators=[
        DataRequired(), 
        Length(min=3, max=200, message='Name must be between 3 and 200 characters')
    ])
    description = TextAreaField('Description', validators=[
        Length(max=1000, message='Description cannot exceed 1000 characters')
    ])
    prompt = TextAreaField('Image Prompt', validators=[
        Length(max=500, message='Prompt cannot exceed 500 characters')
    ])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    subcategory = SelectField('Subcategory', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update Image')

class SearchForm(FlaskForm):
    search_query = StringField('Search Images', validators=[
        Length(max=200, message='Search query cannot exceed 200 characters')
    ])
    category = SelectField('Category', coerce=int)
    subcategory = SelectField('Subcategory', coerce=int)
    submit = SubmitField('Search')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[
        DataRequired(),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    submit = SubmitField('Save Category')

class SubcategoryForm(FlaskForm):
    name = StringField('Subcategory Name', validators=[
        DataRequired(),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    category = SelectField('Parent Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save Subcategory')

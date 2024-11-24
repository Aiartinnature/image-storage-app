"""
Routes Module for the Image Storage Application.

This module defines all the URL routes and view functions for the application.
It handles:
- Image upload, viewing, editing, and deletion
- Category and subcategory management
- Image search functionality
- API endpoints for dynamic content
"""

import os
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, abort, jsonify
from werkzeug.utils import secure_filename
from sqlalchemy import or_

from app.models import db, Category, Subcategory, Image
from app.forms import ImageUploadForm, ImageEditForm, SearchForm, CategoryForm, SubcategoryForm

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    Display the home page with paginated recent images.
    
    Returns:
        str: Rendered index.html template with paginated images
    """
    try:
        page = request.args.get('page', 1, type=int)
        images = Image.query.order_by(Image.upload_date.desc()).paginate(
            page=page, 
            per_page=current_app.config['IMAGES_PER_PAGE']
        )
        return render_template('index.html', images=images)
    except Exception as e:
        flash(f'Error loading images: {str(e)}', 'error')
    finally:
        db.session.close()

@bp.route('/upload', methods=['GET', 'POST'])
def upload_image():
    """
    Handle image upload functionality.
    
    GET: Display the upload form
    POST: Process the uploaded image and metadata
    
    Returns:
        str: Rendered upload form or redirect to image details
    """
    form = ImageUploadForm()
    
    try:
        # Dynamically populate category and subcategory choices
        form.category.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
        form.subcategory.choices = [(s.id, s.name) for s in Subcategory.query.order_by(Subcategory.name).all()]
        
        if form.validate_on_submit():
            try:
                # Handle file upload
                file = form.image.data
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                
                # Save the file
                file.save(filepath)
                
                # Create new image record
                new_image = Image(
                    name=form.name.data,
                    filename=filename,
                    description=form.description.data,
                    prompt=form.prompt.data,
                    category_id=form.category.data,
                    subcategory_id=form.subcategory.data
                )
                
                db.session.add(new_image)
                db.session.commit()
                
                flash('Image uploaded successfully!', 'success')
                return redirect(url_for('main.image_details', image_id=new_image.id))
                
            except Exception as e:
                flash(f'Error uploading image: {str(e)}', 'error')
                db.session.rollback()
        
        return render_template('upload.html', form=form)
        
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('main.index'))
    finally:
        db.session.close()

@bp.route('/image/<int:image_id>')
def image_details(image_id):
    """
    Display details of a specific image.
    
    Args:
        image_id (int): ID of the image to display
        
    Returns:
        str: Rendered image details template
    """
    try:
        image = Image.query.get_or_404(image_id)
        return render_template('image_details.html', image=image)
    except Exception as e:
        flash(f'Error loading image: {str(e)}', 'error')
    finally:
        db.session.close()

@bp.route('/image/<int:image_id>/edit', methods=['GET', 'POST'])
def edit_image(image_id):
    """
    Edit an existing image's metadata.
    
    Args:
        image_id (int): ID of the image to edit
        
    Returns:
        str: Rendered edit form or redirect to image details
    """
    try:
        image = Image.query.get_or_404(image_id)
        form = ImageEditForm(obj=image)
        
        # Populate category and subcategory choices
        form.category.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
        form.subcategory.choices = [(s.id, s.name) for s in Subcategory.query.order_by(Subcategory.name).all()]
        
        if form.validate_on_submit():
            try:
                # Update image metadata manually instead of using populate_obj
                image.name = form.name.data
                image.description = form.description.data
                image.prompt = form.prompt.data
                image.category_id = form.category.data
                image.subcategory_id = form.subcategory.data
                
                db.session.commit()
                
                flash('Image updated successfully!', 'success')
                return redirect(url_for('main.image_details', image_id=image.id))
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating image: {str(e)}', 'error')
    except Exception as e:
        flash(f'Error loading image: {str(e)}', 'error')
        return redirect(url_for('main.index'))
    finally:
        db.session.close()
    
    return render_template('edit_image.html', form=form, image=image)

@bp.route('/image/<int:image_id>/delete', methods=['POST'])
def delete_image(image_id):
    """
    Delete an image.
    
    Args:
        image_id (int): ID of the image to delete
        
    Returns:
        str: Redirect to home page
    """
    try:
        image = Image.query.get_or_404(image_id)
        
        # Delete image file from filesystem
        image.delete_file()
        
        # Remove from database
        db.session.delete(image)
        db.session.commit()
        
        flash('Image deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting image: {str(e)}', 'error')
    finally:
        db.session.close()
    
    return redirect(url_for('main.index'))

@bp.route('/api/subcategories/<int:category_id>')
def get_subcategories(category_id):
    """
    API endpoint to get subcategories for a category.
    
    Args:
        category_id (int): ID of the category
        
    Returns:
        str: JSON response with subcategory data
    """
    try:
        subcategories = Subcategory.query.filter_by(category_id=category_id).order_by(Subcategory.name).all()
        return jsonify([{
            'id': sub.id,
            'name': sub.name
        } for sub in subcategories])
    except Exception as e:
        flash(f'Error loading subcategories: {str(e)}', 'error')
    finally:
        db.session.close()

@bp.route('/search', methods=['GET'])
def search_images():
    """
    Search images by various criteria.
    
    Supported search parameters:
    - Query string (searches name and description)
    - Category
    - Subcategory
    - Date range
    
    Returns:
        str: Rendered search results template
    """
    form = SearchForm(request.args)
    
    try:
        # Populate category and subcategory choices
        form.category.choices = [(0, 'All Categories')] + \
            [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
        form.subcategory.choices = [(0, 'All Subcategories')] + \
            [(s.id, s.name) for s in Subcategory.query.order_by(Subcategory.name).all()]
        
        images = []
        
        # Process search if there are any query parameters
        if request.args:
            query = Image.query
            
            # Search by query string
            if form.search_query.data:
                search_term = f"%{form.search_query.data}%"
                query = query.filter(or_(
                    Image.name.ilike(search_term),
                    Image.description.ilike(search_term),
                    Image.prompt.ilike(search_term)
                ))
            
            # Filter by category
            if form.category.data and form.category.data != 0:
                query = query.filter(Image.category_id == form.category.data)
            
            # Filter by subcategory
            if form.subcategory.data and form.subcategory.data != 0:
                query = query.filter(Image.subcategory_id == form.subcategory.data)
            
            images = query.order_by(Image.upload_date.desc()).all()
        
        return render_template('search.html', form=form, images=images)
    except Exception as e:
        flash(f'Error loading search results: {str(e)}', 'error')
    finally:
        db.session.close()

@bp.route('/categories')
def categories():
    """
    List all categories and subcategories.
    
    Returns:
        str: Rendered categories template
    """
    try:
        categories = Category.query.order_by(Category.name).all()
        return render_template('categories/list.html', categories=categories)
    except Exception as e:
        flash(f'Error loading categories: {str(e)}', 'error')
    finally:
        db.session.close()

@bp.route('/categories/new', methods=['GET', 'POST'])
def new_category():
    """
    Create a new category.
    
    Returns:
        str: Rendered category form or redirect to categories list
    """
    form = CategoryForm()
    
    try:
        if form.validate_on_submit():
            category = Category(name=form.name.data)
            db.session.add(category)
            db.session.commit()
            flash('Category created successfully!', 'success')
            return redirect(url_for('main.categories'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating category: {str(e)}', 'error')
    finally:
        db.session.close()
    
    return render_template('categories/form.html', form=form, title='New Category')

@bp.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    """
    Edit an existing category.
    
    Args:
        category_id (int): ID of the category to edit
        
    Returns:
        str: Rendered category form or redirect to categories list
    """
    try:
        category = Category.query.get_or_404(category_id)
        form = CategoryForm(obj=category)
        
        if form.validate_on_submit():
            try:
                category.name = form.name.data
                db.session.commit()
                flash('Category updated successfully!', 'success')
                return redirect(url_for('main.categories'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating category: {str(e)}', 'error')
    except Exception as e:
        flash(f'Error loading category: {str(e)}', 'error')
        return redirect(url_for('main.categories'))
    finally:
        db.session.close()
    
    return render_template('categories/form.html', form=form, category=category, title='Edit Category')

@bp.route('/categories/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    """
    Delete a category and its subcategories.
    
    Args:
        category_id (int): ID of the category to delete
        
    Returns:
        str: Redirect to categories list
    """
    try:
        category = Category.query.get_or_404(category_id)
        
        # Check if category has any images
        if category.images:
            flash('Cannot delete category that contains images. Move or delete the images first.', 'danger')
            return redirect(url_for('main.categories'))
        
        # Delete subcategories
        for subcategory in category.subcategories:
            db.session.delete(subcategory)
        
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting category: {str(e)}', 'error')
    finally:
        db.session.close()
    
    return redirect(url_for('main.categories'))

@bp.route('/subcategories/new', methods=['GET', 'POST'])
def new_subcategory():
    """
    Create a new subcategory.
    
    Returns:
        str: Rendered subcategory form or redirect to categories list
    """
    form = SubcategoryForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    
    try:
        if form.validate_on_submit():
            subcategory = Subcategory(
                name=form.name.data,
                category_id=form.category.data
            )
            db.session.add(subcategory)
            db.session.commit()
            flash('Subcategory created successfully!', 'success')
            return redirect(url_for('main.categories'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating subcategory: {str(e)}', 'error')
    finally:
        db.session.close()
    
    return render_template('categories/subcategory_form.html', form=form, title='New Subcategory')

@bp.route('/subcategories/<int:subcategory_id>/edit', methods=['GET', 'POST'])
def edit_subcategory(subcategory_id):
    """
    Edit an existing subcategory.
    
    Args:
        subcategory_id (int): ID of the subcategory to edit
        
    Returns:
        str: Rendered subcategory form or redirect to categories list
    """
    try:
        subcategory = Subcategory.query.get_or_404(subcategory_id)
        form = SubcategoryForm(obj=subcategory)
        form.category.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
        
        if form.validate_on_submit():
            try:
                subcategory.name = form.name.data
                subcategory.category_id = form.category.data
                db.session.commit()
                flash('Subcategory updated successfully!', 'success')
                return redirect(url_for('main.categories'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating subcategory: {str(e)}', 'error')
    except Exception as e:
        flash(f'Error loading subcategory: {str(e)}', 'error')
        return redirect(url_for('main.categories'))
    finally:
        db.session.close()
    
    return render_template('categories/subcategory_form.html', form=form, subcategory=subcategory, title='Edit Subcategory')

@bp.route('/subcategories/<int:subcategory_id>/delete', methods=['POST'])
def delete_subcategory(subcategory_id):
    """
    Delete a subcategory.
    
    Args:
        subcategory_id (int): ID of the subcategory to delete
        
    Returns:
        str: Redirect to categories list
    """
    try:
        subcategory = Subcategory.query.get_or_404(subcategory_id)
        
        # Check if subcategory has any images
        if subcategory.images:
            flash('Cannot delete subcategory that contains images. Move or delete the images first.', 'danger')
            return redirect(url_for('main.categories'))
        
        db.session.delete(subcategory)
        db.session.commit()
        flash('Subcategory deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting subcategory: {str(e)}', 'error')
    finally:
        db.session.close()
    
    return redirect(url_for('main.categories'))

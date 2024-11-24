# Image Storage Web Application

## Overview
This is a comprehensive image storage and management web application built with Flask and MySQL. The application allows users to upload, categorize, search, and manage their image collection with robust metadata support.

## Features
- Image Upload with Metadata
- Categorization and Sub-categorization
- Advanced Search Functionality
- Image Details and Management
- Pagination of Image Gallery

## Prerequisites
- Python 3.8+
- MySQL Server
- pip (Python Package Manager)

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/image-storage-app.git
cd image-storage-app
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure Database
- Create a MySQL database named `image_storage_db`
- Update `config.py` with your database credentials

5. Set Environment Variables
```bash
export FLASK_APP=run.py
export FLASK_ENV=development
export DATABASE_URL=mysql://username:password@localhost/image_storage_db
```

6. Initialize the Database
```bash
flask db upgrade
```

7. Run the Application
```bash
python run.py
```

## Usage
- Navigate to `http://localhost:5000`
- Upload images with metadata
- Categorize and search your images
- Edit or delete images as needed

## API Documentation

### Image Management Endpoints

#### GET /
- **Description**: Home page displaying paginated recent images
- **Query Parameters**:
  - `page` (optional): Page number for pagination (default: 1)
- **Response**: HTML page with recent images

#### GET /image/{image_id}
- **Description**: View details of a specific image
- **Parameters**:
  - `image_id`: ID of the image to display
- **Response**: HTML page with image details

#### POST /upload
- **Description**: Upload a new image
- **Form Data**:
  - `name`: Display name for the image
  - `image`: Image file
  - `description` (optional): Image description
  - `prompt` (optional): AI prompt used to generate the image
  - `category`: Category ID
  - `subcategory`: Subcategory ID
- **Response**: Redirects to image details page on success

#### POST /image/{image_id}/edit
- **Description**: Update image metadata
- **Parameters**:
  - `image_id`: ID of the image to edit
- **Form Data**:
  - `name`: New display name
  - `description` (optional): New description
  - `prompt` (optional): New AI prompt
  - `category`: New category ID
  - `subcategory`: New subcategory ID
- **Response**: Redirects to image details page on success

#### POST /image/{image_id}/delete
- **Description**: Delete an image
- **Parameters**:
  - `image_id`: ID of the image to delete
- **Response**: Redirects to home page on success

### Search Endpoints

#### GET /search
- **Description**: Search for images using various criteria
- **Query Parameters**:
  - `query` (optional): Search term for name/description/prompt
  - `category` (optional): Filter by category ID
  - `subcategory` (optional): Filter by subcategory ID
  - `page` (optional): Page number for pagination
- **Response**: HTML page with search results

### Category Management Endpoints

#### GET /categories
- **Description**: List all categories and their subcategories
- **Response**: HTML page with category listing

#### POST /categories/new
- **Description**: Create a new category
- **Form Data**:
  - `name`: Category name
- **Response**: Redirects to categories list on success

#### POST /categories/{category_id}/edit
- **Description**: Update a category
- **Parameters**:
  - `category_id`: ID of the category to edit
- **Form Data**:
  - `name`: New category name
- **Response**: Redirects to categories list on success

#### POST /categories/{category_id}/delete
- **Description**: Delete a category and its subcategories
- **Parameters**:
  - `category_id`: ID of the category to delete
- **Response**: Redirects to categories list on success

### Subcategory Management Endpoints

#### POST /subcategories/new
- **Description**: Create a new subcategory
- **Form Data**:
  - `name`: Subcategory name
  - `category`: Parent category ID
- **Response**: Redirects to categories list on success

#### POST /subcategories/{subcategory_id}/edit
- **Description**: Update a subcategory
- **Parameters**:
  - `subcategory_id`: ID of the subcategory to edit
- **Form Data**:
  - `name`: New subcategory name
  - `category`: New parent category ID
- **Response**: Redirects to categories list on success

#### POST /subcategories/{subcategory_id}/delete
- **Description**: Delete a subcategory
- **Parameters**:
  - `subcategory_id`: ID of the subcategory to delete
- **Response**: Redirects to categories list on success

### AJAX Endpoints

#### GET /api/subcategories/{category_id}
- **Description**: Get subcategories for a specific category
- **Parameters**:
  - `category_id`: ID of the category
- **Response**: JSON array of subcategories
  ```json
  [
    {
      "id": 1,
      "name": "Subcategory Name"
    }
  ]
  ```

### Sample API Usage

Here are examples of how to interact with the API using different methods:

#### Viewing an Image

```python
# Python example using requests
import requests

def get_image_details(image_id):
    url = f'http://localhost:5000/image/{image_id}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text  # Returns HTML content
    else:
        print(f"Error: {response.status_code}")
        return None

# Usage
image_details = get_image_details(1)
```

```bash
# cURL example
curl -X GET http://localhost:5000/image/1
```

#### Uploading an Image

```python
# Python example using requests
import requests

def upload_image(image_path, name, category_id, subcategory_id, description=None, prompt=None):
    url = 'http://localhost:5000/upload'
    
    # Prepare the file and form data
    files = {
        'image': open(image_path, 'rb')
    }
    
    data = {
        'name': name,
        'category': category_id,
        'subcategory': subcategory_id,
        'description': description,
        'prompt': prompt
    }
    
    response = requests.post(url, files=files, data=data)
    
    if response.status_code == 302:  # Successful redirect
        print("Upload successful!")
        return True
    else:
        print(f"Error: {response.status_code}")
        return False

# Usage
success = upload_image(
    image_path='path/to/image.jpg',
    name='My Image',
    category_id=1,
    subcategory_id=2,
    description='A beautiful landscape',
    prompt='Mountain lake at sunset'
)
```

```bash
# cURL example
curl -X POST http://localhost:5000/upload \
  -F "image=@path/to/image.jpg" \
  -F "name=My Image" \
  -F "category=1" \
  -F "subcategory=2" \
  -F "description=A beautiful landscape" \
  -F "prompt=Mountain lake at sunset"
```

#### Searching Images

```python
# Python example using requests
import requests

def search_images(query=None, category=None, subcategory=None, page=1):
    url = 'http://localhost:5000/search'
    
    params = {
        'page': page
    }
    
    if query:
        params['query'] = query
    if category:
        params['category'] = category
    if subcategory:
        params['subcategory'] = subcategory
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.text  # Returns HTML content
    else:
        print(f"Error: {response.status_code}")
        return None

# Usage
# Search for images with "sunset" in their name/description
results = search_images(query="sunset", category=1, page=1)
```

```bash
# cURL example
curl -X GET "http://localhost:5000/search?query=sunset&category=1&page=1"
```

#### Getting Subcategories (AJAX)

```python
# Python example using requests
import requests

def get_subcategories(category_id):
    url = f'http://localhost:5000/api/subcategories/{category_id}'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Returns list of subcategories
    else:
        print(f"Error: {response.status_code}")
        return None

# Usage
subcategories = get_subcategories(1)
if subcategories:
    for subcat in subcategories:
        print(f"ID: {subcat['id']}, Name: {subcat['name']}")
```

```bash
# cURL example
curl -X GET http://localhost:5000/api/subcategories/1
```

These examples demonstrate basic usage of the API endpoints. Remember to:
- Replace `localhost:5000` with your actual server address if different
- Handle errors appropriately in production code
- Add proper authentication if implemented
- Use secure HTTPS in production

For JavaScript usage in the browser, you can use the Fetch API:

```javascript
// Example: Get subcategories using Fetch API
async function getSubcategories(categoryId) {
    try {
        const response = await fetch(`/api/subcategories/${categoryId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

// Usage
getSubcategories(1)
    .then(subcategories => {
        if (subcategories) {
            subcategories.forEach(subcat => {
                console.log(`ID: ${subcat.id}, Name: ${subcat.name}`);
            });
        }
    });
```

### Response Status Codes

- `200 OK`: Request successful
- `302 Found`: Successful redirect after form submission
- `400 Bad Request`: Invalid input data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

### Error Handling

All endpoints include error handling that will:
1. Display user-friendly error messages via flash messages
2. Rollback database transactions on failure
3. Clean up uploaded files if database operations fail
4. Return appropriate HTTP status codes
5. Log errors for debugging

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

# Configuration Guide

This guide explains how to configure and customize the Image Storage Application to meet your specific needs.

## Configuration Files

The application uses several configuration files:

1. `.env` - Environment variables
2. `config.py` - Application configuration
3. `.gitignore` - Version control settings

## Environment Variables

### Essential Variables
Create or modify `.env` file in the root directory:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secure-secret-key
DATABASE_URL=sqlite:///app.db
UPLOAD_FOLDER=app/static/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB in bytes
```

### Optional Variables
```env
DEBUG=True
TESTING=False
LOG_LEVEL=INFO
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,webp,svg
ITEMS_PER_PAGE=12
```

## Application Configuration (config.py)

### Database Configuration
```python
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### File Upload Settings
```python
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'app/static/uploads'
MAX_CONTENT_LENGTH = os.environ.get('MAX_CONTENT_LENGTH') or 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
```

### Pagination Settings
```python
ITEMS_PER_PAGE = os.environ.get('ITEMS_PER_PAGE') or 12
```

## Category Configuration

### Default Categories
The application comes with predefined categories:

1. Personal
   - Family
   - Friends
   - Events
   - Travel

2. Work
   - Projects
   - Meetings
   - Documents
   - Screenshots

3. Art
   - Digital
   - Traditional
   - Sketches
   - Paintings

4. Photography
   - Landscape
   - Portrait
   - Street
   - Nature

5. Design
   - UI/UX
   - Graphics
   - Logos
   - Mockups

### Customizing Categories

1. Modify the default categories in `app/models.py`
2. Run database migrations:
```bash
flask db migrate -m "Update categories"
flask db upgrade
```

## Security Configuration

### Secret Key
Generate a secure secret key:
```python
import secrets
print(secrets.token_hex(16))
```

Add it to your `.env` file:
```env
SECRET_KEY=your-generated-secret-key
```

### File Upload Security
Configure allowed file types in `config.py`:
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
```

### Maximum File Size
Adjust the maximum file size in `.env`:
```env
MAX_CONTENT_LENGTH=16777216  # 16MB
```

## Development Configuration

### Debug Mode
Enable debug mode in `.env`:
```env
FLASK_ENV=development
DEBUG=True
```

### Testing Configuration
Set testing environment in `.env`:
```env
TESTING=True
DATABASE_URL=sqlite:///test.db
```

## Production Configuration

### Production Settings
Update `.env` for production:
```env
FLASK_ENV=production
DEBUG=False
TESTING=False
```

### Database Configuration
For production, consider using a more robust database:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Logging Configuration
Configure logging in `config.py`:
```python
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
```

## Performance Tuning

### Database Optimization
```python
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_MAX_OVERFLOW = 20
SQLALCHEMY_POOL_TIMEOUT = 30
```

### Caching Configuration
```python
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 300
```

## Next Steps

1. Review the [User Guide](User-Guide) for usage instructions
2. Check the [API Documentation](API-Documentation) for integration details
3. Visit the [Development Guide](Development-Guide) for customization options

## Troubleshooting

If you encounter configuration issues:
1. Verify all required environment variables are set
2. Check file permissions for upload directory
3. Ensure database connection string is correct
4. Review the [Troubleshooting](Troubleshooting) guide

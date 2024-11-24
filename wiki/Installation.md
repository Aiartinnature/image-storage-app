# Installation Guide

This guide will walk you through the process of setting up the Image Storage Application on your system.

## Prerequisites

Before installation, ensure you have:
- Python 3.8 or higher installed
- pip (Python package installer)
- Git (for cloning the repository)
- 100MB+ free disk space
- Administrator privileges (for Windows users)

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Aiartinnature/image-storage-app.git
cd image-storage-app
```

### 2. Create Virtual Environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/MacOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database

```bash
python create_dirs.py
flask db upgrade
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory with the following content:
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

### 6. Start the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Verifying Installation

1. Open your web browser
2. Navigate to `http://localhost:5000`
3. You should see the application's home page
4. Try uploading an image to verify functionality

## Server Management

### Starting the Server
```bash
python run.py
```

### Stopping the Server
Windows users can use the provided script:
```bash
stop_servers.bat
```

For Linux/MacOS users, use:
```bash
pkill -f "python run.py"
```

## Common Installation Issues

### Port 5000 Already in Use
Run the stop_servers script or manually terminate the process using:
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Database Initialization Errors
1. Delete the existing `app.db` file
2. Run database initialization commands again:
```bash
flask db upgrade
```

### Package Installation Errors
1. Upgrade pip:
```bash
python -m pip install --upgrade pip
```
2. Try installing requirements again:
```bash
pip install -r requirements.txt
```

## Next Steps

1. Visit the [Configuration Guide](Configuration) to customize your installation
2. Read the [User Guide](User-Guide) to learn how to use the application
3. Check the [Troubleshooting](Troubleshooting) guide if you encounter any issues

## Support

If you encounter installation problems:
1. Check the [Troubleshooting](Troubleshooting) guide
2. Search existing GitHub issues
3. Create a new issue with:
   - Your operating system and version
   - Python version
   - Full error message
   - Steps to reproduce the issue

"""
Entry point for the Image Storage Application.

This module creates and runs the Flask application instance using the
application factory pattern. It configures the app in debug mode when
run directly.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Run the application in debug mode when executed directly
    app.run(debug=True)

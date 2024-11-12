"""
ciobrain/__init__.py

This module initialized the Flask application, sets up configuration settings,
creates necessary directories, and registers the main Blueprints for the admin
and customer sections.
"""

import os
from flask import Flask, render_template
from ciobrain.admin import admin_bp
from ciobrain.customer import customer_bp

def create_app(test_config=None):
    """Initialize and configure the Flask app instance"""

    app = Flask(__name__, instance_relative_config=True)

    # Ensure the 'instance' directory is created
    os.makedirs(app.instance_path, exist_ok=True)

    # Default configuration settings
    app.config.from_mapping(
        SECRET_KEY='dev',  # Replace with a better default if needed
        ORIGINAL_UPLOADS_FOLDER='document_storage/original_uploads',
        IN_PROGRESS_FOLDER='document_storage/in_progress',
        FINAL_STAGING_FOLDER='document_storage/final_staging',
        ALLOWED_EXTENSIONS={'.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx'}
    )

    # Load configurations from file if it exists
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_pyfile(test_config)

    # Create necessary directories
    directories = [
        app.config.get('ORIGINAL_UPLOADS_FOLDER'),
        app.config.get('IN_PROGRESS_FOLDER'),
        app.config.get('FINAL_STAGING_FOLDER')
    ]
    for directory in directories:
        if directory:
            try:
                os.makedirs(directory, exist_ok=True)
            except OSError as e:
                app.logger.error("Error creating directory %s: %s", directory, e)

    # Define homepage route
    @app.route('/')
    def home():
        return render_template('index.html')

    # Register Blueprints
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(customer_bp, url_prefix='/customer')
    return app

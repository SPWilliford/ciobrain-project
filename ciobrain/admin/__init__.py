"""
ciobrain/admin/__init__.py

Defines admin Blueprint and routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from ciobrain.admin.documents import DocumentsManager

documents_manager = DocumentsManager()

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def home():
    """Admin dashboard homepage"""
    return render_template('admin_home.html')

@admin_bp.route('/documents')
def documents():
    """Document management page"""
    directories = documents_manager.get_directories()
    return render_template('admin_documents.html', directories = directories)

@admin_bp.route('documents/upload', methods=['POST'])
def upload_document():
    """document upload operation"""
    file = request.files.get('file')
    if file:
        try:
            documents_manager.upload_document(file)
            flash("File uploaded successfully!", "success")
        except ValueError as e:
            flash(str(e), "error")
    else:
        flash("No file selected!", "error")
    return redirect(url_for('admin.documents'))

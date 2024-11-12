"""
ciobrain/customer/__init__.py

Defines the customer Blueprint and routes
"""
from flask import Blueprint, render_template

customer_bp = Blueprint('customer', __name__, '/customer')

@customer_bp.route('/')
def home():
    """main customer dahsboard page"""
    return render_template('customer_home.html')

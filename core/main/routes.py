#!/usr/bin/env python3
'''
    File location: /core/main/routes.py
    Declares landing page main routes
'''

from flask import render_template
from flask_login import login_required, current_user
from core.main import main_bp
from core.extensions import db

@main_bp.route('/')
def index():
    """
    Landing page
    """
    return render_template('index.html')

@main_bp.route('/profile')
@login_required
def profile():
    """
    Current user's profile
    """

    # Get the current user's first name
    first_name = current_user.first_name
    return render_template('profile.html', first_name=first_name)

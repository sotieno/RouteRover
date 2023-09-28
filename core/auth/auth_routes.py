#!/usr/bin/env python3
'''
    File location: /core/auth/auth_routes.py
    Declares authorization routes
'''

import secrets
from core.auth import auth_bp
from core.main import main_bp
from flask import jsonify, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from core.models.user import User
from core.utils.functions import is_valid_email, is_valid_password, get_password_requirements
from werkzeug.security import check_password_hash


# Login users
@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login_post():
    # Extract login data from the request
    username_or_email = request.form.get("login_input")
    password = request.form.get("password")
    remember = True if request.form.get('remember') else False

    # Find the user by email or username
    user = User.query.filter((User.email == username_or_email) | (User.username == username_or_email)).first()

    # Check if a user was found and if the password is correct
    if user and check_password_hash(user.password_hash, password):
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
    else:
        flash('Incorrect username or password.')
        return redirect(url_for('auth.login'))

# Register users
@auth_bp.route('/signup')
def signup():
    '''
    This endpoint renders the registration form
    '''
    return render_template('signup.html', password_requirements=get_password_requirements())

@auth_bp.route('/signup', methods=['POST', 'GET'])
def signup_user():
    '''
    This endpoint allows users to register with a username,
    email, first_name, last_name and password.
    '''

    # Handle GET request to display the signup form
    if request.method == 'GET':
        return render_template('signup.html', password_requirements=get_password_requirements())

    # Extract user data from the request
    username = request.form.get("username")
    email = request.form.get("email")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    password = request.form.get("password")

    # Validate email and password
    if not is_valid_email(email):
        error_message = 'Invalid email address'
    elif not is_valid_password(password):
        error_message = 'Invalid password'
    else:
        # Check if the username or email already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            error_message = 'Username already exists'
        elif existing_email:
            error_message = 'Email address already exists'
        else:
            # Create a new user instance
            new_user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )

            # Add the user to the database
            from core.extensions import db
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('auth.login'))

    # If any validation checks fail, render the signup form with error message and password requirements
    return render_template('signup.html', error=flash(error_message), password_requirements=get_password_requirements())


# Logout users
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

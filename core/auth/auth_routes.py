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
    return render_template('signup.html')

@auth_bp.route('/signup', methods=['POST'])
def signup_user():
    '''
    This endpoint allows users to register with a username,
    email, first_name, last_name and password.
    '''

    # Extract user data from the request
    username = request.form.get("username")
    email = request.form.get("email")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    password = request.form.get("password")

    # Check if the username or email already exists in the database
    existing_user = User.query.filter_by(username=username).first()
    existing_email = User.query.filter_by(email=email).first()

    if existing_user:
        flash('Username already exists')
        return redirect(url_for('auth.signup'))
    if existing_email:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

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

# Logout users
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

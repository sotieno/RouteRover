#!/usr/bin/env python3
'''
    File location: /core/models/user.py
    Declares User model
'''

from flask_login import UserMixin
from core.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """
    User model
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(
        255), unique=True, nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.TIMESTAMP, server_default=db.func.now())
    last_updated_at = db.Column(
        db.TIMESTAMP, onupdate=db.func.current_timestamp())

    def __init__(self, username, email, first_name, last_name, password):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User "{self.username}">'

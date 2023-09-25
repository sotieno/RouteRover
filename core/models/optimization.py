#!/usr/bin/env python3
'''
    File location: /core/models/optimization.py
    Declares OptimizedRoute model
'''

from core.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class OptimizedRoute(db.Model):
    __tablename__ = 'optimized_routes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    route = db.Column(db.Geometry('LINESTRING', srid=4326), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now(), nullable=False)

    # Define the relationship with the User model
    user = relationship('User', back_populates='optimized_routes')

    def __init__(self, user_id, route):
        self.user_id = user_id
        self.route = route

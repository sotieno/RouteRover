from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


from core.auth import auth_routes

from flask import Blueprint

get_route_bp = Blueprint('route', __name__, url_prefix='/route')


from core.optimization import get_routes

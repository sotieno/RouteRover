from flask import Blueprint

delivery_bp = Blueprint('deliveries', __name__, url_prefix='/deliveries')


from core.deliveries import delivery_routes

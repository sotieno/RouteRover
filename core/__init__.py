from flask import Flask
from config import Config
from core.extensions import db
from flask_login import LoginManager

def create_app(config_class=Config):
    '''
    Initializes and registers blueprints
    '''
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initializing Flask extensions
    db.init_app(app)

    # Registering blueprints
    from core.main import main_bp # main blueprint
    app.register_blueprint(main_bp)

    from core.auth import auth_bp # auth blueprint
    app.register_blueprint(auth_bp)

    from core.optimization import get_route_bp # optimization blueprint
    app.register_blueprint(get_route_bp)

    from core.deliveries import delivery_bp # deliveries blueprint
    app.register_blueprint(delivery_bp)

    # Specify user loader
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from core.models.user import User

    @login_manager.user_loader
    def load_user(id):
        # Get the user
        return User.query.get(int(id))

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app

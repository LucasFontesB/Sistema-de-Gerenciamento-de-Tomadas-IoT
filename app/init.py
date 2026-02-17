from flask import Flask
from app.config import Config
from app.routes.dispositivos_routes import dispositivos_bp
from app.database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        init_db()

    app.register_blueprint(dispositivos_bp)

    return app
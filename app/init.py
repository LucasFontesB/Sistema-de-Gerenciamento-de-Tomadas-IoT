from flask import Flask
from app.config import Config
from app.routes.dispositivos_routes import dispositivos_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(dispositivos_bp)

    return app
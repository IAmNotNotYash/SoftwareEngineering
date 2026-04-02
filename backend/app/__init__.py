from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Load config
    env = os.environ.get("FLASK_ENV", "development")
    from app.config import config_map
    app.config.from_object(config_map[env])

    # Init extensions
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints (add more as you build them)
    # from app.routes.auth import auth_bp
    # app.register_blueprint(auth_bp, url_prefix="/api/auth")
    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    @app.route("/")
    def index():
        return {"message": "Welcome to the Backend API. Access /health for status."}, 200

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app

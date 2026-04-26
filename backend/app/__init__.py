from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()

def create_app():
    app = Flask(__name__)

    # Load config
    env = os.environ.get("FLASK_ENV", "development")
    from app.config import config_map
    app.config.from_object(config_map[env])

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # JWT Debug Loaders
    @jwt.unauthorized_loader
    def unauthorized_response(callback):
        print(f"DEBUG JWT: Missing/Unauthorized: {callback}")
        return {"error": "Missing Authorization Header", "msg": callback}, 401

    @jwt.invalid_token_loader
    def invalid_token_response(callback):
        print(f"DEBUG JWT: Invalid Token: {callback}")
        return {"error": "Invalid Token Format", "msg": callback}, 422

    @jwt.expired_token_loader
    def expired_token_response(jwt_header, jwt_payload):
        print(f"DEBUG JWT: Expired Token: {jwt_payload}")
        return {"error": "Token Expired"}, 401

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        import json
        from app.models.user import User
        try:
            identity = json.loads(jwt_data["sub"])
            user = db.session.get(User, identity["id"])
            if not user or user.is_suspended:
                return None
            if user.role == 'artist' and user.artist_profile.verification_status == 'rejected':
                return None
            return user
        except Exception:
            return None

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    from app.routes.commerce import commerce_bp
    app.register_blueprint(commerce_bp, url_prefix="/api/commerce")

    from app.routes.catalogue import catalogue_bp
    app.register_blueprint(catalogue_bp, url_prefix="/api/catalogues")

    from app.routes.social import social_bp
    app.register_blueprint(social_bp, url_prefix="/api/social")

    from app.routes.communication import communication_bp
    app.register_blueprint(communication_bp, url_prefix="/api/communication")

    from app.routes.analytics import analytics_bp
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")

    @app.route("/")
    def index():
        return {"message": "Welcome to the Backend API. Access /health for status."}, 200

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app

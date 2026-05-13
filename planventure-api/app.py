import os

from flask import Flask, jsonify
from flask_cors import CORS

from auth import auth_bp
from auth_middleware import get_current_user, require_auth
from config import Config
from extensions import db, jwt
from trips import trips_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configure CORS for React frontend
    # This allows the React development server (localhost:3000) to make requests
    # to the Flask API with proper CORS headers for authentication and data transfer
    cors_config = {
        "origins": app.config['CORS_ORIGINS'],  # Default: http://localhost:3000, http://127.0.0.1:3000
        "methods": app.config['CORS_METHODS'],  # GET, POST, PUT, DELETE, OPTIONS
        "headers": ["Content-Type", "Authorization"],  # Allow JWT tokens and JSON content
        "credentials": True,  # Allow cookies and authorization headers
        "expose_headers": ["Content-Type", "Authorization"]  # Expose response headers
    }
    CORS(app, **cors_config)

    db.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(trips_bp, url_prefix='/trips')

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to PlanVenture API"})

    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"})

    @app.route('/db-status')
    def db_status():
        return jsonify({
            "database_uri": app.config["SQLALCHEMY_DATABASE_URI"],
            "initialized": True,
        })

    @app.route('/protected')
    @require_auth
    def protected():
        user = get_current_user()
        return jsonify({
            "message": "This is a protected route",
            "user": user.to_dict() if user else None
        })

    return app


app = create_app()

if __name__ == '__main__':
    debug_mode = os.getenv("FLASK_DEBUG", "1") in ("1", "true", "True")
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug_mode)

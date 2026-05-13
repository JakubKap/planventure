import os

from flask import Flask, jsonify
from flask_cors import CORS

from auth import auth_bp
from config import Config
from extensions import db, jwt

from auth_middleware import get_current_user, require_auth

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')

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

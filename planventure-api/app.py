import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

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

    return app


app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    debug_mode = os.getenv("FLASK_DEBUG", "1") in ("1", "true", "True")
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug_mode)

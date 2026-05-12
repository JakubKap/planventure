from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# Shared extensions for the Flask application
# Avoids circular imports between app.py and model modules.
db = SQLAlchemy()
jwt = JWTManager()

from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from utils import create_password_hash, verify_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationship to trips
    trips = db.relationship('Trip', backref='user', lazy=True)

    def set_password(self, password: str, method: str = 'werkzeug') -> None:
        """Set the user's password hash using the specified method.

        Args:
            password: The plain text password
            method: Hashing method ('werkzeug' or 'pbkdf2')
        """
        self.password_hash = create_password_hash(password, method)

    def check_password(self, password: str) -> bool:
        """Verify a password against the stored hash.

        Args:
            password: The plain text password to verify

        Returns:
            True if password matches, False otherwise
        """
        return verify_password_hash(password, self.password_hash)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"


class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    destination = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    coordinates = db.Column(db.String(255))  # Store as "lat,lng" or JSON string
    itinerary = db.Column(db.Text)  # JSON string containing trip itinerary
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationship back to user
    user = db.relationship('User', backref=db.backref('trips', lazy=True))

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'destination': self.destination,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'coordinates': self.coordinates,
            'itinerary': self.itinerary,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f"<Trip id={self.id} destination={self.destination} user_id={self.user_id}>"

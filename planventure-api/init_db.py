#!/usr/bin/env python3
"""
Database initialization script for PlanVenture API.

This script creates all database tables defined in the models.
Run this script to set up the database schema.
"""

from app import create_app

def init_db():
    """Initialize the database by creating all tables."""
    app = create_app()

    with app.app_context():
        from extensions import db
        db.create_all()
        print("✅ Database tables created successfully!")
        print(f"📍 Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

if __name__ == "__main__":
    init_db()
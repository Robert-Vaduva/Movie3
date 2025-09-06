"""
Database models for the movie tracking application.

This module defines the SQLAlchemy models used to represent application data:
- User: represents a registered user of the system, storing their basic info.
- Movie: represents a movie entry associated with a user, including title,
  director, release year, and poster URL.

Relationships:
- A User can have many Movies (one-to-many).
- Each Movie belongs to exactly one User.

These models are used by the DataManager and Flask routes to persist and
query data in the underlying database.
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


db = SQLAlchemy()


class User(db.Model):  # pylint: disable=too-few-public-methods
    """Database model representing an application user."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    # relationships
    movies = relationship("Movie", back_populates="users")

    def __repr__(self):
        return f"User(id = {self.id}, name = {self.name})"


class Movie(db.Model):  # pylint: disable=too-few-public-methods
    """Database model representing a movie entry associated with a user."""
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String)
    release = db.Column(db.String)
    poster_url = db.Column(db.String)
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    # relationships
    users = relationship("User", back_populates="movies")

    def __repr__(self):
        return f"Movie(id = {self.id}, name = {self.title})"

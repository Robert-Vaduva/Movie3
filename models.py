from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


db = SQLAlchemy()


class User(db.Model):  # pylint: disable=too-few-public-methods
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    # relationships
    movies = relationship("Movie", back_populates="users")

    def __repr__(self):
        return f"User(id = {self.id}, name = {self.name})"


class Movie(db.Model):  # pylint: disable=too-few-public-methods
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

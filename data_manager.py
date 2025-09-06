"""
Data management layer for the movie tracking application.

This module defines the DataManager class, which provides a high-level
interface for interacting with the database using SQLAlchemy. It handles
CRUD operations for the application's core models:

- User: represents a registered user of the system.
- Movie: represents a movie entry associated with a user, including title,
  director, release date, and poster URL.

Responsibilities:
- Creating and retrieving users.
- Fetching all movies for a given user.
- Adding new movies by integrating with the external API helper
  (`get_movie_info`) to fetch movie metadata.
- Updating existing movie titles.
- Deleting movies belonging to a user.

Error Handling:
All database interactions are wrapped in exception handling. On failure,
the session is rolled back to maintain consistency, and the methods return
safe fallback values (e.g., None, [], or False).
"""
from sqlalchemy.exc import SQLAlchemyError
from models import db, User, Movie
from helpers.api.api_helper import get_movie_info


class DataManager():
    """Provides CRUD operations for User and Movie database models."""
    def create_user(self, name):
        """Create and persist a new user with the given name."""
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return None

    def get_users(self):
        """Retrieve all users from the database."""
        try:
            return db.session.query(User).all()
        except SQLAlchemyError as e:
            print(f"Error fetching users: {e}")
            return []

    def get_movies(self, user_id):
        """Retrieve all movies belonging to a given user."""
        try:
            return db.session.query(Movie).filter_by(user_id=user_id).all()
        except SQLAlchemyError as e:
            print(f"Error fetching movies for user {user_id}: {e}")
            return []

    def add_movie(self, user_id, title):
        """Fetch movie details and add a new movie for the given user."""
        try:
            title, director, release, poster = get_movie_info(title)
            movie_2_add = Movie(
                title=title,
                director=director,
                release=release,
                poster_url=poster,
                user_id=user_id
            )
            db.session.add(movie_2_add)
            db.session.commit()
            return movie_2_add
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error adding movie: {e}")
            return None
        except (ValueError, KeyError) as e:
            # Catch errors from get_movie_info
            print(f"Error fetching movie info: {e}")
            return None

    def update_movie(self, user_id, movie_id, new_title):
        """Update the title of a user's movie by ID."""
        try:
            movie_2_update = db.session.query(Movie).filter_by(
                id=movie_id, user_id=user_id
            ).first()
            if not movie_2_update:
                print(f"Movie {movie_id} for user {user_id} not found.")
                return None

            movie_2_update.title = new_title
            db.session.commit()
            return movie_2_update
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating movie {movie_id}: {e}")
            return None

    def delete_movie(self, user_id, movie_id):
        """Delete a user's movie by ID."""
        try:
            movie_2_delete = db.session.query(Movie).filter_by(
                id=movie_id, user_id=user_id
            ).first()
            if not movie_2_delete:
                print(f"Movie {movie_id} for user {user_id} not found.")
                return False

            db.session.delete(movie_2_delete)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting movie {movie_id}: {e}")
            return False

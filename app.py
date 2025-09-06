"""
Flask web application for managing users and their movie collections.

Provides routes to view, add, update, and delete users and movies,
with data stored in a SQLite database via SQLAlchemy.

Key features:
- List all users and their movies.
- Add, update, and delete movies for a user.
- Add new users.

Uses the DataManager class for database interactions and creates
tables on startup if they do not exist.
"""
import os
from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db, User


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
data_manager = DataManager()  # Create an object of your DataManager class


@app.route('/')
def index():
    """Render the home page with a list of all users."""
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users')
def list_users():
    """Return a string representation of all users."""
    users = data_manager.get_users()
    return str(users)


@app.route('/users', methods=['POST'])
def add_user():
    """Create a new user and redirect to the home page."""
    name = request.form.get('name')
    data_manager.create_user(name)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id):
    """Render a page with all movies for the specified user."""
    user = db.session.query(User).filter_by(id=user_id).first()
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user=user)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Add a new movie for the specified user."""
    title = request.form.get('title')
    data_manager.add_movie(user_id=user_id, title=title)
    return redirect(url_for('list_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Update the title of a user's movie."""
    title = request.form.get('title')
    data_manager.update_movie(user_id, movie_id, title)
    return redirect(url_for('list_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Delete a movie belonging to the specified user."""
    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('list_movies', user_id=user_id))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()

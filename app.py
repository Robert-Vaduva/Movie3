import os
from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db, Movie, User


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
data_manager = DataManager()  # Create an object of your DataManager class


@app.route('/')
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users')
def list_users():
    users = data_manager.get_users()
    return str(users)


@app.route('/users', methods=['POST'])
def add_user():
    name = request.form.get('name')
    data_manager.create_user(name)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user=user)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    title = request.form.get('title')
    data_manager.add_movie(user_id=user_id, title=title)
    return redirect(url_for('list_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    return "Welcome to MoviWeb App!"


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    return "Welcome to MoviWeb App!"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()

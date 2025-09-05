from models import db, User, Movie
from helpers.api.api_helper import get_movie_info
from datetime import date


class DataManager():
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        return db.session.query(User).all()

    def get_movies(self, user_id):
        return db.session.query(Movie).filter_by(user_id=user_id).all()

    def add_movie(self, user_id, title):
        title, director, release, poster = get_movie_info(title)
        movie_2_add = Movie(title=title, director=director,
                            release=release,
                            poster_url=poster, user_id=user_id)
        db.session.add(movie_2_add)
        db.session.commit()

    def update_movie(self, movie_id, new_title):
        movie_2_update = db.session.query(Movie).filter_by(id=movie_id).first()
        movie_2_update.title = new_title
        db.session.commit()

    def delete_movie(self, movie_id):
        movie_2_delete = db.session.query(Movie).filter_by(id=movie_id).first()
        db.session.delete(movie_2_delete)
        db.session.commit()

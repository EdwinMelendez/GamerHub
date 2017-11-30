from GamerHub import app
from flask_sqlalchemy import SQLAlchemy

# creating SQLAlchemy database
db = SQLAlchemy(app)

# todo: edit database models to store more information about the games and user
# todo: add methods for updating profile information i.e.(password & username)


# User Model class, sets up database columns and metadata
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    games = db.relationship('Tracked_Games', backref='user', lazy='dynamic')

    # constructor method
    def __init__(self, user_name, password, email):
        self.user_name = user_name
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User: %r>' % self.user_name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

class Tracked_Games(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(50), nullable=False, unique=True)
    tracker = db.Column(db.String(50), db.ForeignKey('user.user_name'), unique=True)

    def __init__(self, game_name, user):
        self.game_name = game_name
        self.tracker = user

    def __repr__(self):
        return '<Game: %r>' % self.game_name


class Query():

    def find_user_id(user_id):
        r = User.query.filter_by(user_id=user_id).first()
        return r

    def find_user_name(user_name):
        r = User.query.filter_by(user_name=user_name).first()
        return r

    def find_game(game_name):
        r = Tracked_Games.query.filter_by(game_name=game_name).first()
        return r

    def find_user_games(user_id):
        r = User.query.filter_by(user_id=user_id).first()
        game_list = []

        for i in r.games.all():
            game_list.append(i)

        return game_list

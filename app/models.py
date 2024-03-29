from app import db
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta


class Image(db.Model):
    """This class represents the Images table."""

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    beginnerPieces = db.relationship('PieceBeginner', backref='image', lazy='dynamic')
    intermediatePieces = db.relationship('PieceIntermediate', backref='image', lazy='dynamic')
    hardPieces = db.relationship('PieceHard', backref='image', lazy='dynamic')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, url, user_id):
        """initialize with url."""
        self.url = url
        if user_id:
            self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Image.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Image: {}>".format(self.id)

class PieceBeginner(db.Model):
    """This class represents the Beginner Pieces table."""

    __tablename__ = 'pieces_beginner'

    id = db.Column(db.Integer, primary_key=True)
    img_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    value = db.Column(db.Integer)
    url = db.Column(db.String(255))

    def __init__(self, img_id, value, url):
        """initialize."""
        self.img_id = img_id
        self.value = value
        self.url = url


    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return PieceBeginner.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Img: {}, Beginner Piece {}: {}>".format(self.img_id, self.value , self.url)


class PieceIntermediate(db.Model):
    """This class represents the Intermediate Pieces table."""

    __tablename__ = 'pieces_intermediate'

    id = db.Column(db.Integer, primary_key=True)
    img_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    value = db.Column(db.Integer)
    url = db.Column(db.String(255))

    def __init__(self, img_id, value, url):
        """initialize."""
        self.img_id = img_id
        self.value = value
        self.url = url


    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return PieceIntermediate.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Img: {}, Intermediate Piece {}: {}>".format(self.img_id, self.value , self.url)

class PieceHard(db.Model):
    """This class represents the Hard Pieces table."""

    __tablename__ = 'pieces_hard'

    id = db.Column(db.Integer, primary_key=True)
    img_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    value = db.Column(db.Integer)
    url = db.Column(db.String(255))

    def __init__(self, img_id, value, url):
        """initialize."""
        self.img_id = img_id
        self.value = value
        self.url = url


    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return PieceHard.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Img: {}, Hard Piece {}: {}>".format(self.img_id, self.value , self.url)

class Tile(db.Model):
    """This class represents the Tiles table."""

    __tablename__ = 'tiles'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    
    def __init__(self, url):
        """initialize with url."""
        self.url = url

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Tile.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Tile {}: {}>".format(self.id, self.url)

class Game(db.Model):
    """This class represents the Games table."""

    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    img_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_completed = db.Column(db.DateTime,
        onupdate=db.func.current_timestamp())
    score = db.Column(db.Time)
    t1 = db.Column(db.Integer)
    t2 = db.Column(db.Integer)
    t3 = db.Column(db.Integer)
    t4 = db.Column(db.Integer)
    t5 = db.Column(db.Integer)
    t6 = db.Column(db.Integer)
    t7 = db.Column(db.Integer)
    t8 = db.Column(db.Integer)
    t9 = db.Column(db.Integer)
    t10 = db.Column(db.Integer)
    t11 = db.Column(db.Integer)
    t12 = db.Column(db.Integer)
    t13 = db.Column(db.Integer)
    t14 = db.Column(db.Integer)
    t15 = db.Column(db.Integer)
    t16 = db.Column(db.Integer)
    win_img = db.Column(db.String(255))

    def __init__(self, img_id, rel, win_img, user_id):
        """initialize with img_id."""
        self.img_id = img_id
        self.user_id = user_id
        self.t1 = rel[0]
        self.t2 = rel[1]
        self.t3 = rel[2]
        self.t4 = rel[3]
        if len(rel)>4:
            self.t5 = rel[4]
            self.t6 = rel[5]
            self.t7 = rel[6]
            self.t8 = rel[7]
            self.t9 = rel[8]
        if len(rel)>9:
            self.t10 = rel[9]
            self.t11 = rel[10]
            self.t12 = rel[11]
            self.t13 = rel[12]
            self.t14 = rel[13]
            self.t15 = rel[14]
            self.t16 = rel[15]
        self.win_img = win_img

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Game.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Game: {}>".format(self.id)

class User(db.Model):
    """This class defines the users table """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False, unique=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    image = db.relationship('Image', lazy='dynamic')
    games = db.relationship('Game', lazy='dynamic')

    def __init__(self, email, username, name, password):
        """Initialize the user with an email and a password."""
        self.email = email
        self.password = password
        self.username = username
        self.name = name

    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<User: {}>".format(self.id)

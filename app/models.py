from app import db


class Image(db.Model):
    """This class represents the Images table."""

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    beginnerPieces = db.relationship('PieceBeginner', backref='image', lazy='dynamic')
    intermediatePieces = db.relationship('PieceIntermediate', backref='image', lazy='dynamic')
    hardPieces = db.relationship('PieceHard', backref='image', lazy='dynamic')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, url):
        """initialize with url."""
        self.url = url

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
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_completed = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    score = db.Column(db.Time)
    one = db.Column(db.Integer)
    two = db.Column(db.Integer)
    three = db.Column(db.Integer)
    four = db.Column(db.Integer)
    win_img = db.Column(db.String(255))

    def __init__(self, img_id, one, two, three, four, win_img):
        """initialize with img_id."""
        self.img_id = img_id
        self.one = one
        self.two = two
        self.three = three
        self.four= four
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

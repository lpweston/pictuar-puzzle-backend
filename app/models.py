from app import db


class Image(db.Model):
    """This class represents the Images table."""

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    beginnerPieces = db.relationship('PieceBeginner', backref='image', lazy='dynamic')
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
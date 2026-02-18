from . import db

class User(db.Model):
    """Model for user accounts."""

    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(64), index=True, unique=True, nullable=False)
    email=db.Column(db.String(80), index=True, unique=True, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)
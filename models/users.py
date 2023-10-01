from main import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    # Define one-to-many relationship with Diaries
    diaries = db.relationship(
        'Diary',
        back_populates='user',
        cascade="all, delete",
        lazy=True
    )
    comments = db.relationship(
        'Comment',
        back_populates='user',
        cascade="all, delete",
        lazy=True
    )
    likes = db.relationship(
        'Like',
        back_populates='user',
        cascade="all, delete",
        lazy=True
    )

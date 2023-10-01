from main import db


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    entries = db.relationship(
        'Entry',
        back_populates='tags',
        secondary='entry_tags',
        lazy=True
    )

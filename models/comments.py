from main import db


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.id'),
                         nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    # Define many-to-one relationship with User
    user = db.relationship(
        'User',
        back_populates='comments',
        lazy=True
    )

    # Define many-to-one relationship with Entry
    entry = db.relationship(
        'Entry',
        back_populates='comments',
        lazy=True
    )


from main import db


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.id'),
                         nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    # Define many-to-one relationship with User
    user = db.relationship(
        'User',
        back_populates='likes',
        lazy=True
    )

    # Define many-to-one relationship with Entry
    entry = db.relationship(
        'Entry',
        back_populates='likes',
        lazy=True
    )


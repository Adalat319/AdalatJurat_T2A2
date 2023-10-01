from enum import Enum

from main import db


class PrivacyOptions(Enum):
    PRIVATE = 'PRIVATE'
    PUBLIC = 'PUBLIC'


class Diary(db.Model):
    __tablename__ = "diaries"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    privacy = db.Column(db.Enum(PrivacyOptions), nullable=False,
                        default=PrivacyOptions.PRIVATE)
    date_created = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship(
        'User',
        back_populates='diaries',
        lazy=True
    )
    # Define one-to-many relationship with Entries
    entries = db.relationship(
        'Entry',
        back_populates='diary',
        cascade="all, delete",
        lazy=True
    )

    @property
    def is_public(self):
        return self.privacy == PrivacyOptions.PUBLIC

    def entries_count(self):
        return len(self.entries)

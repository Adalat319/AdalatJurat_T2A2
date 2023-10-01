from main import db


class EntryTag(db.Model):
    __tablename__ = "entry_tags"

    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.id'),
                         nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'),
                       nullable=False)

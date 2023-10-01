from main import db


class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    diary_id = db.Column(db.Integer, db.ForeignKey('diaries.id'),
                         nullable=False)

    diary = db.relationship(
        'Diary',
        back_populates='entries',
        lazy=True
    )
    # Define many-to-many relationship with Tags
    tags = db.relationship(
        'Tag',
        back_populates='entries',
        secondary='entry_tags',
        lazy=True
    )

    # Define one-to-many relationship with Comments
    comments = db.relationship(
        'Comment',
        back_populates='entry',
        cascade="all, delete",
        lazy=True
    )

    # Define one-to-many relationship with Likes
    likes = db.relationship(
        'Like',
        back_populates='entry',
        cascade="all, delete",
        lazy=True
    )

    def add_tag(self, tag):
        if tag in self.tags:
            return False
        self.tags.append(tag)
        return True

    def remove_tag(self, tag):
        if tag not in self.tags:
            return False
        self.tags.remove(tag)
        return True

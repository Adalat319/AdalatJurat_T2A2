from flask import Blueprint
from datetime import datetime

from main import db, bcrypt
from models import User, Diary, Entry, Like, Comment, Tag
from models.diaries import PrivacyOptions

db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables are created")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables are dropped")


@db_commands.cli.command("seed")
def seed_db():
    # create User objects
    user1 = User(
        email="user1@example.com",
        password=bcrypt.generate_password_hash("password").decode("utf-8")
    )
    user2 = User(
        email="user2@example.com",
        password=bcrypt.generate_password_hash("password").decode("utf-8")
    )

    # add all users object to db
    db.session.add_all([
        user1, user2,
    ])
    # commit db for users
    db.session.commit()

    # Create diaries
    diary1 = Diary(
        title="User1 Diary1",
        privacy=PrivacyOptions.PUBLIC,
        user_id=user1.id,
        date_created=datetime.utcnow()
    )
    diary2 = Diary(
        title="User1 Diary2",
        user_id=user1.id,
        date_created=datetime.utcnow()
    )
    diary3 = Diary(
        title="User2 Diary1",
        privacy=PrivacyOptions.PUBLIC,
        user_id=user2.id,
        date_created=datetime.utcnow()
    )
    diary4 = Diary(
        title="User2 Diary2",
        user_id=user2.id,
        date_created=datetime.utcnow()
    )

    # add all diaries object to db
    db.session.add_all([
        diary1, diary2, diary3, diary4
    ])
    # commit db for diaries
    db.session.commit()

    # create entries
    entry1 = Entry(
        content="Diary1 Entry1",
        date_created=datetime.utcnow(),
        diary_id=diary1.id
    )
    entry2 = Entry(
        content="Diary1 Entry2",
        date_created=datetime.utcnow(),
        diary_id=diary1.id
    )
    entry3 = Entry(
        content="Diary2 Entry1",
        date_created=datetime.utcnow(),
        diary_id=diary2.id
    )
    entry4 = Entry(
        content="Diary4 Entry1",
        date_created=datetime.utcnow(),
        diary_id=diary4.id
    )

    # add all entries object to db
    db.session.add_all([
        entry1, entry2, entry3, entry4
    ])
    # commit db for entries
    db.session.commit()

    # create Likes
    like1 = Like(
        user_id=user1.id,
        entry_id=entry1.id,
        date_created=datetime.utcnow()
    )
    like2 = Like(
        user_id=user2.id,
        entry_id=entry1.id,
        date_created=datetime.utcnow()
    )
    like3 = Like(
        user_id=user1.id,
        entry_id=entry3.id,
        date_created=datetime.utcnow()
    )
    like4 = Like(
        user_id=user2.id,
        entry_id=entry4.id,
        date_created=datetime.utcnow()
    )

    # add all likes object to db
    db.session.add_all([
        like1, like2, like3, like4
    ])
    # commit db for likes
    db.session.commit()

    # create Comments
    comment1 = Comment(
        content="Comment by user1 on entry1",
        user_id=user1.id,
        entry_id=entry1.id,
        date_created=datetime.utcnow()
    )
    comment2 = Comment(
        content="Comment by user 1 on entry 2",
        user_id=user1.id,
        entry_id=entry2.id,
        date_created=datetime.utcnow()
    )
    comment3 = Comment(
        content="Comment by user 2 on entry 2",
        user_id=user2.id,
        entry_id=entry2.id,
        date_created=datetime.utcnow()
    )
    comment4 = Comment(
        content="Comment by user 2 on entry 3",
        user_id=user2.id,
        entry_id=entry3.id,
        date_created=datetime.utcnow()
    )

    # add all likes object to db
    db.session.add_all([
        comment1, comment2, comment3, comment4
    ])
    # commit db for likes
    db.session.commit()

    # create Tags
    tag1 = Tag(
        name="Tag1"
    )
    tag2 = Tag(
        name="Tag2"
    )

    # add all likes object to db
    db.session.add_all([
        tag1, tag2
    ])
    # commit db for likes
    db.session.commit()

    # Add tag to entries
    entry1.tags.append(tag1)
    entry1.tags.append(tag2)
    entry2.tags.append(tag1)
    entry3.tags.append(tag2)

    # commit db for tag entry
    db.session.commit()

    # log if seed is succeeded
    print("Database has been seeded")

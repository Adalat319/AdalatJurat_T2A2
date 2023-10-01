from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError, DataError

from main import db
from models import User, Entry
from models.likes import Like
from schemas.likes import like_schema, likes_schema

# Create a Blueprint for likes
likes = Blueprint("likes", __name__, url_prefix="/likes")


# Add your controller functions here

@likes.errorhandler(KeyError)
def key_error_handler(e):
    return jsonify({"error": f"Key Error - `{e}`"}), 400


@likes.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"error": f"Integrity Error - `{e}`"}), 400


@likes.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"error": f"Data Error - `{e}`"}), 400


# Add your controller functions here
@likes.route("/entries/<int:entry_id>", methods=["GET"])
def get_likes(entry_id: int):
    # Query the "entries" table in the database for a record with the given
    # id and get the record found (None if no record found).
    entry = Entry.query.get(entry_id)
    if entry:
        # Query the "likes" table in the database for records with the given
        # entry ID and get all the records found (None if no record found).
        all_likes = db.session.query(Like).filter_by(entry_id=entry_id).all()
        result = likes_schema.dump(all_likes)
        return jsonify(result)

    return jsonify({"message": "Entry not found"}), 404


@likes.route("/<int:like_id>", methods=["GET"])
def get_like(like_id: int):
    # Query the "likes" table in the database for a record with the given
    # id and get the record found (None if no record found).
    like = Like.query.get(like_id)

    if like:
        response = like_schema.dump(like)
        return jsonify(response)

    return jsonify({"message": "Like not found"}), 404


@likes.route("/", methods=["POST"])
@jwt_required()
def create_like():
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()
    like_json = like_schema.load(request.json)
    # Query the "entries" table in the database for a record with the given
    # id and get the record found (None if no record found).
    entry = Entry.query.get(like_json['entry_id'])

    if entry:
        #  Check if the user has already liked the entry
        if any([like.user_id == user.id for like in entry.likes]):
            return (
                jsonify({"message": "The user has already liked this entry."}),
                409  # Conflict
            )
        like = Like(**like_json)
        like.user_id = user.id
        like.date_created = datetime.utcnow()
        db.session.add(like)
        db.session.commit()

        result = like_schema.dump(like)
        return jsonify(result), 201

    return jsonify({"message": "Entry not found"}), 404


@likes.route("/<int:like_id>", methods=["DELETE"])
@jwt_required()
def delete_like(like_id: int):
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()
    # Query the "likes" table in the database for a record with the given
    # id and get the record found (None if no record found).
    like = Like.query.get(like_id)

    if like:
        if like.user_id == user.id:
            db.session.delete(like)
            db.session.commit()
            return jsonify({"message": "Like deleted successfully"})

        return (
            jsonify({"message": "User is not authorized to delete the like"}),
            403  # Forbidden
        )

    return jsonify({"message": "Like not found"}), 404

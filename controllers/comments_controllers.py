from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, DataError

from main import db
from models import User, Entry
from models.comments import Comment
from schemas.comments import comment_schema, comments_schema

# Create a Blueprint for comments
comments = Blueprint("comments", __name__, url_prefix="/comments")


# Add your controller functions here
@comments.errorhandler(KeyError)
def key_error_handler(e):
    return jsonify({"error": f"Key Error - `{e}`"}), 400


@comments.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify({"error": f"Validation error - `{e}`"}), 400


@comments.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"error": f"Integrity Error - `{e}`"}), 400


@comments.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"error": f"Data Error - `{e}`"}), 400


# Add your controller functions here
@comments.route("/entries/<int:entry_id>", methods=["GET"])
def get_comments(entry_id: int):
    # Query the "entries" table in the database for a record with the given
    # id and get the record found (None if no record found).
    entry = Entry.query.get(entry_id)
    if entry:
        # Query the "comments" table in the database for records with the given
        # entry ID and get all the records found (None if no record found).
        all_comments = db.session.query(Comment).filter_by(
            entry_id=entry_id).all()
        result = comments_schema.dump(all_comments)
        return jsonify(result)

    return jsonify({"message": "Entry not found"}), 404


@comments.route("/<int:comment_id>", methods=["GET"])
def get_comment(comment_id: int):
    # Query the "comments" table in the database for a record with the given
    # id and get the record found (None if no record found).
    comment = Comment.query.get(comment_id)

    if comment:
        response = comment_schema.dump(comment)
        return jsonify(response)

    return jsonify({"message": "Comment not found"}), 404


@comments.route("/", methods=["POST"])
@jwt_required()
def create_comment():
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()
    comment_json = comment_schema.load(request.json)
    # Query the "entries" table in the database for a record with the given
    # id and get the record found (None if no record found).
    entry = Entry.query.get(comment_json['entry_id'])

    if entry:
        comment = Comment(**comment_json)
        comment.user_id = user.id
        comment.date_created = datetime.utcnow()
        db.session.add(comment)
        db.session.commit()

        result = comment_schema.dump(comment)
        return jsonify(result), 201

    return jsonify({"message": "Entry not found"}), 404


@comments.route("/<int:comment_id>", methods=["PUT"])
@jwt_required()
def update_comment(comment_id: int):
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()
    # Query the "comments" table in the database for a record with the given
    # id and get the record found (None if no record found).
    comment = Comment.query.get(comment_id)

    if comment:
        if comment.user_id == user.id:
            comment_data = comment_schema.load(request.json)
            comment.content = comment_data['content']
            db.session.commit()
            result = comment_schema.dump(comment)
            return jsonify(result)
        return (
            jsonify(
                {"message": "User is not authorized to update the comment"}
            ),
            403  # Forbidden
        )

    return jsonify({"message": "Comment not found"}), 404


@comments.route("/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id: int):
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()
    # Query the "comments" table in the database for a record with the given
    # id and get the record found (None if no record found).
    comment = Comment.query.get(comment_id)

    if comment:
        if comment.user_id == user.id:
            db.session.delete(comment)
            db.session.commit()
            return jsonify({"message": "Comment deleted successfully"})

        return (
            jsonify({
                "message": "User is not authorized to delete the comment"}
            ),
            403  # Forbidden
        )

    return jsonify({"message": "Comment not found"}), 404

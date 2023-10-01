from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, DataError

from main import db
from models import Tag, User, Diary
from models.diaries import PrivacyOptions
from models.entries import Entry
from schemas.entries import entry_schema, entries_schema

# Create a Blueprint for entries
entries = Blueprint("entries", __name__, url_prefix="/entries")


@entries.errorhandler(KeyError)
def key_error_handler(e):
    return jsonify({"error": f"Key Error - `{e}`"}), 400


@entries.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify({"error": f"Validation error - `{e}`"}), 400


@entries.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"error": f"Integrity Error - `{e}`"}), 400


@entries.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"error": f"Data Error - `{e}`"}), 400


# Add your controller functions here
@entries.route("/diaries/<int:diary_id>", methods=["GET"])
@jwt_required()
def get_entries(diary_id: int):
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()
    # Query the "diaries" table in the database for a record with the given
    # id and get the record found (None if no record found).
    diary = Diary.query.get(diary_id)

    if diary:
        if diary.user_id == user.id:
            # Query the "entries" table in the database for records with the
            # given diary ID and get all the records found
            # (None if no record found).
            all_entries = db.session.query(Entry).filter_by(
                diary_id=diary_id).all()
            result = entries_schema.dump(all_entries)
            return jsonify(result)

        return (
            jsonify({"message": "User is not authorized to access the diary"}),
            403  # Forbidden
        )

    return jsonify({"message": "Diary not found"}), 404


@entries.route("/<int:entry_id>", methods=["GET"])
@jwt_required()
def get_entry(entry_id: int):
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()
    # Query the "entries" table in the database for a record with the given
    # id and get the record found (None if no record found).
    entry = Entry.query.get(entry_id)

    if entry:
        if entry.diary.user_id == user.id:
            response = entry_schema.dump(entry)
            return jsonify(response)
        return (
            jsonify({"message": "User is not authorized to view the entry"}),
            403  # Forbidden
        )

    return jsonify({"message": "Entry not found"}), 404


@entries.route("/", methods=["POST"])
@jwt_required()
def create_entry():
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()

    entry_json = entry_schema.load(request.json)
    # Query the "diaries" table in the database for a record with the given
    # id and get the record found (None if no record found).
    diary = Diary.query.get(entry_json['diary_id'])

    if diary:
        if diary.user_id == user.id:
            entry = Entry(**entry_json)
            entry.date_created = datetime.utcnow()
            db.session.add(entry)
            db.session.commit()

            result = entry_schema.dump(entry)
            return jsonify(result), 201
        return (
            jsonify({"message": "User is not authorized to create the entry"}),
            403  # Forbidden
        )

    return jsonify({"message": "Diary not found"}), 404


@entries.route("/<int:entry_id>", methods=["PUT"])
@jwt_required()
def update_entry(entry_id: int):
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()
    # Query the "entries" table in the database for a record with the given
    # id and get the record found (None if no record found).
    entry = Entry.query.get(entry_id)

    if entry:
        if entry.diary.user_id == user.id:
            entry_data = entry_schema.load(request.json)
            entry.content = entry_data['content']
            db.session.commit()
            result = entry_schema.dump(entry)
            return jsonify(result)

        return (
            jsonify({"message": "User is not authorized to update the entry"}),
            403  # Forbidden
        )

    return jsonify({"message": "Entry not found"}), 404


@entries.route("/<int:entry_id>", methods=["DELETE"])
@jwt_required()
def delete_entry(entry_id: int):
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()
    # Query the "entries" table in the database for a record with the given
    # id and get the record found (None if no record found).
    entry = Entry.query.get(entry_id)

    if entry:
        if entry.diary.user_id == user.id:
            db.session.delete(entry)
            db.session.commit()
            return jsonify({"message": "Entry deleted successfully"})

        return (
            jsonify({"message": "User is not authorized to delete the entry"}),
            403  # Forbidden
        )

    return jsonify({"message": "Entry not found"}), 404


@entries.route("/<int:entry_id>/tags/<int:tag_id>", methods=["PUT"])
@jwt_required()
def add_tag(entry_id: int, tag_id: int):
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()
    # Query the "entries" table in the database for a record with the given
    # id and get the record found (None if no record found).
    entry = Entry.query.get(entry_id)
    # Query the "tags" table in the database for a record with the given
    # id and get the record found (None if no record found).
    tag = Tag.query.get(tag_id)

    if not entry:
        return jsonify({"message": "Entry not found"}), 404

    if not tag:
        return jsonify({"message": "Tag not found"}), 404

    if entry.diary.user_id != user.id:
        return (
            jsonify({"message": "User is not authorized to update the entry"}),
            403  # Forbidden
        )

    is_added = entry.add_tag(tag)

    if not is_added:
        return (jsonify({"message": "The tag already exists on this entry"}),
                409)

    entry.tags.append(tag)
    db.session.commit()
    result = entry_schema.dump(entry)
    return jsonify(result)


@entries.route("/<int:entry_id>/tags/<int:tag_id>", methods=["DELETE"])
@jwt_required()
def remove_tag(entry_id: int, tag_id: int):
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()
    # Query the "entries" table in the database for a record with the given
    # id and get the record found (None if no record found).
    entry = Entry.query.get(entry_id)
    # Query the "tags" table in the database for a record with the given
    # id and get the record found (None if no record found).
    tag = Tag.query.get(tag_id)

    if not entry:
        return jsonify({"message": "Entry not found"}), 404

    if not tag:
        return jsonify({"message": "Tag not found"}), 404

    if entry.diary.user_id != user.id:
        return (
            jsonify({"message": "User is not authorized to update the entry"}),
            403  # Forbidden
        )

    is_removed = entry.remove_tag(tag)

    if not is_removed:
        return (jsonify({"message": "The tag does not exists on this entry"}),
                400)

    entry.tags.remove(tag)
    db.session.commit()
    result = entry_schema.dump(entry)
    return jsonify(result)


@entries.route("/tags/<int:tag_id>", methods=["GET"])
def get_entries_by_tag(tag_id: int):
    # Query the "tags" table in the database for a record with the given
    # id and get the record found (None if no record found).
    tag = Tag.query.get(tag_id)

    if tag:
        #  Filter out all the entries belonging to PRIVATE diaries
        all_public_entries = [entry for entry in tag.entries if
                              entry.diary.privacy == PrivacyOptions.PUBLIC]

        result = entries_schema.dump(all_public_entries)
        return jsonify(result)

    return jsonify({"message": "Tag not found"}), 404

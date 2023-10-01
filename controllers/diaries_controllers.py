from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, DataError

from main import db
from models import User
from models.diaries import Diary
from schemas.diaries import diary_schema, diaries_schema

# Create a Blueprint for diaries
diaries = Blueprint("diaries", __name__, url_prefix="/diaries")


@diaries.errorhandler(KeyError)
def key_error_handler(e):
    return jsonify({"error": f"Key Error - `{e}`"}), 400


@diaries.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify({"error": f"Validation error - `{e}`"}), 400


@diaries.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"error": f"Integrity Error - `{e}`"}), 400


@diaries.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"error": f"Data Error - `{e}`"}), 400


# Add your controller functions here
@diaries.route("/", methods=["GET"])
@jwt_required()
def get_diaries():
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()

    # Query the "diaries" table in the database for records with the given
    # user ID and get all the records found (None if no record found).
    all_diaries = db.session.query(Diary).filter_by(user_id=user.id).all()
    result = diaries_schema.dump(all_diaries)
    return jsonify(result)


@diaries.route("/<int:diary_id>", methods=["GET"])
@jwt_required()
def get_diary(diary_id: int):
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()
    # Query the "diaries" table in the database for a record with the given
    # id and get the record found (None if no record found).
    diary = Diary.query.get(diary_id)

    if diary:
        if diary.user_id == user.id:
            response = diary_schema.dump(diary)
            return jsonify(response)
        return (
            jsonify({"message": "User is not authorized to view the diary"}),
            403  # Forbidden
        )

    return jsonify({"message": "Diary not found"}), 404


@diaries.route("/", methods=["POST"])
@jwt_required()
def create_diary():
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()

    diary_json = diary_schema.load(request.json)
    diary = Diary(**diary_json)
    diary.user_id = user.id
    diary.date_created = datetime.utcnow()
    db.session.add(diary)
    db.session.commit()

    result = diary_schema.dump(diary)
    return jsonify(result), 201  # Created


@diaries.route("/<int:diary_id>", methods=["PUT"])
@jwt_required()
def update_diary(diary_id: int):
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()
    # Query the "diaries" table in the database for a record with the given
    # id and get the record found (None if no record found).
    diary = Diary.query.get(diary_id)

    if diary:
        if diary.user_id == user.id:
            diary_data = diary_schema.load(request.json)
            diary.title = diary_data['title']
            if diary_data.get('privacy'):
                diary.privacy = diary_data['privacy']
            db.session.commit()
            result = diary_schema.dump(diary)
            return jsonify(result)

        return (
            jsonify({"message": "User is not authorized to update the diary"}),
            403  # Forbidden
        )

    return jsonify({"message": "Diary not found"}), 404


@diaries.route("/<int:diary_id>", methods=["DELETE"])
@jwt_required()
def delete_diary(diary_id: int):
    email = get_jwt_identity()
    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()
    # Query the "diaries" table in the database for a record with the given
    # id and get the record found (None if no record found).
    diary = Diary.query.get(diary_id)

    if diary:
        if diary.user_id == user.id:
            db.session.delete(diary)
            db.session.commit()
            return jsonify({"message": "Diary deleted successfully"})

        return (
            jsonify({"message": "User is not authorized to delete the diary"}),
            403  # Forbidden
        )

    return jsonify({"message": "Diary not found"}), 404

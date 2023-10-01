from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, DataError

from main import db, bcrypt
from models.users import User
from schemas.users import user_schema

# /auth
auths = Blueprint("auth", __name__, url_prefix="/auth")


@auths.errorhandler(KeyError)
def key_error_handler(e):
    return jsonify({"error": f"Key Error - `{e}`"}), 400


@auths.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify({"error": f"Validation error - `{e}`"}), 400


@auths.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"error": f"Integrity Error - `{e}`"}), 400


@auths.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"error": f"Data Error - `{e}`"}), 400


@auths.route("/register", methods=["POST"])
def register_user():
    user_json = user_schema.load(request.json)

    user = User(
        **{
            "email": user_json["email"],
            "password": (
                bcrypt.generate_password_hash(user_json["password"])
                .decode("utf")
            )
        }
    )
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user_json["email"])

    return jsonify(access_token=access_token)


@auths.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    # Query the "users" table in the database for a record with the given
    # email and get the first record found (None if no record found).
    user = db.session.query(User).filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Incorrect username and password!"}), 401

    access_token = create_access_token(identity=request.json["email"])

    return jsonify(access_token=access_token)

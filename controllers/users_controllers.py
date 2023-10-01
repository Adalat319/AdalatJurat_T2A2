from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError, DataError

from main import db, bcrypt
from models.users import User
from schemas.users import user_schema, users_schema

# /users
users = Blueprint("users", __name__, url_prefix="/users")


@users.errorhandler(KeyError)
def key_error_handler(e):
    return jsonify({"error": f"Key Error - `{e}`"}), 400


@users.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify({"error": f"Validation error - `{e}`"}), 400


@users.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"error": f"Integrity Error - `{e}`"}), 400


@users.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"error": f"Data Error - `{e}`"}), 400


# GET all users
@users.route("/", methods=["GET"])
def get_users():
    # Query the "users" table in the database get all records found (None if no
    # record found).
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


# GET a single user by ID
@users.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    # Query the "users" table in the database for a record with the given
    # id and get the record found (None if no record found).
    user = User.query.get(user_id)

    if user:
        result = user_schema.dump(user)
        return jsonify(result)

    return jsonify({"message": "User not found"}), 404


# CREATE a new user
@users.route("/", methods=["POST"])
def create_user():
    try:
        user = user_schema.load(request.json)

        password_hash = (
            bcrypt.generate_password_hash(user["password"]).decode("utf")
        )
        user = User(**user)
        user.password = password_hash
        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user)
        return jsonify(result), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400


# UPDATE a user by ID
@users.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    # Query the "users" table in the database for a record with the given
    # id and get the record found (None if no record found).
    user = User.query.get(user_id)

    if user:
        user_data = user_schema.load(request.json)
        user.email = user_data["email"]
        user.password = (
            bcrypt.generate_password_hash(user_data["password"]).decode("utf")
        )
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify(result)

    return jsonify({"message": "User not found"}), 404


# DELETE a user by ID
@users.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    # Query the "users" table in the database for a record with the given
    # id and get the record found (None if no record found).
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})

    return jsonify({"message": "User not found"}), 404

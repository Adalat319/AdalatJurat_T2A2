from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, DataError

from main import db
from models.tags import Tag
from schemas.tags import tag_schema, tags_schema

# /tags
tags = Blueprint("tags", __name__, url_prefix="/tags")


@tags.errorhandler(KeyError)
def key_error_handler(e):
    return jsonify({"error": f"Key Error - `{e}`"}), 400


@tags.errorhandler(ValidationError)
def validation_error_handler(e):
    return jsonify({"error": f"Validation error - `{e}`"}), 400


@tags.errorhandler(IntegrityError)
def integrity_error_handler(e):
    return jsonify({"error": f"Integrity Error - `{e}`"}), 400


@tags.errorhandler(DataError)
def data_error_handler(e):
    return jsonify({"error": f"Data Error - `{e}`"}), 400


# Add your controller functions here
@tags.route("/", methods=["GET"])
def get_tags():
    # Query the "tags" table in the database and get all the records found
    # (None if no record found).
    all_tags = Tag.query.all()
    result = tags_schema.dump(all_tags)
    return jsonify(result)


@tags.route("/<int:tag_id>", methods=["GET"])
def get_tag(tag_id: int):
    # Query the "tags" table in the database for a record with the given
    # id and get the record found (None if no record found).
    tag = Tag.query.get(tag_id)

    if tag:
        response = tag_schema.dump(tag)
        return jsonify(response)

    return jsonify({"message": "Tag not found"}), 404


@tags.route("/", methods=["POST"])
def create_tag():
    tag_json = tag_schema.load(request.json)
    tag = Tag(**tag_json)
    db.session.add(tag)
    db.session.commit()

    result = tag_schema.dump(tag)
    return jsonify(result), 201


@tags.route("/<int:tag_id>", methods=["PUT"])
def update_tag(tag_id: int):
    # Query the "tags" table in the database for a record with the given
    # id and get the record found (None if no record found).
    tag = Tag.query.get(tag_id)

    if tag:
        tag_data = tag_schema.load(request.json)
        tag.name = tag_data['name']
        db.session.commit()
        result = tag_schema.dump(tag)
        return jsonify(result)

    return jsonify({"message": "Tag not found"}), 404


@tags.route("/<int:tag_id>", methods=["DELETE"])
def delete_tag(tag_id: int):
    # Query the "tags" table in the database for a record with the given
    # id and get the record found (None if no record found).
    tag = Tag.query.get(tag_id)

    if tag:
        db.session.delete(tag)
        db.session.commit()
        return jsonify({"message": "Tag deleted successfully"})

    return jsonify({"message": "Tag not found"}), 404

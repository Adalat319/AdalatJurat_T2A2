from main import ma
from marshmallow import fields, validate
from models.tags import Tag
from schemas.common import TrimmedString


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag

    id = fields.Int(dump_only=True)
    name = TrimmedString(required=True, validate=validate.Length(
        min=1, error="Tag name cannot be empty")
                         )
    entries = fields.Nested('EntrySchema', many=True,
                            exclude=('tags', 'likes', 'comments'))


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)

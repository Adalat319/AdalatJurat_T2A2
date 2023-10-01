from main import ma
from marshmallow import fields, validate
from models.entries import Entry
from schemas.common import TrimmedString


class EntrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Entry
        include_relationships = True

    id = fields.Int(dump_only=True)
    content = TrimmedString(required=True, validate=validate.Length(
        min=1, error="Entry content cannot be empty")
                            )  # Sanitize and validate content
    date_created = fields.DateTime(dump_only=True)
    diary_id = fields.Int(required=True, load_only=True)
    diary = fields.Nested('DiarySchema', exclude=('entries',))
    tags = fields.Nested('TagSchema', many=True, exclude=('entries',))
    comments = fields.Nested('CommentSchema', many=True,
                             exclude=('entry', 'entry_id'))
    likes = fields.Nested('LikeSchema', many=True,
                          exclude=('entry', 'entry_id'))


entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True)

from main import ma
from marshmallow import fields, validate
from models.comments import Comment
from schemas.common import TrimmedString


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment

    id = fields.Int(dump_only=True)
    content = TrimmedString(required=True, validate=validate.Length(
        min=1, error="Comment cannot be empty")
                            )  # Sanitize and validate content
    entry_id = fields.Int(required=True, load_only=True)
    date_created = fields.DateTime(dump_only=True)
    user = fields.Nested('UserSchema',
                         exclude=('likes', 'comments', 'diaries'))
    entry = fields.Nested('EntrySchema',
                          exclude=('likes', 'comments', 'tags'))


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

from main import ma
from marshmallow import fields
from models.likes import Like


class LikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Like
        include_relationships = True

    id = fields.Int(dump_only=True)
    entry_id = fields.Int(required=True, load_only=True)
    date_created = fields.DateTime(dump_only=True)
    user = fields.Nested('UserSchema',
                         exclude=('likes', 'comments', 'diaries'))
    entry = fields.Nested('EntrySchema',
                          exclude=('likes', 'comments', 'tags'))


like_schema = LikeSchema()
likes_schema = LikeSchema(many=True)

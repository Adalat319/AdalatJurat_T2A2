from main import ma
from marshmallow import fields, validate
from models.users import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True

    id = fields.Int(dump_only=True)
    email = fields.Email(
        required=True, validate=validate.Email(
            error="Not a valid email address")
    )
    password = fields.Str(
        required=True, load_only=True, validate=validate.Length(
            min=6, error="Password must be at least 6 characters long")
    )
    diaries = fields.Nested('DiarySchema', many=True,
                            exclude=('user', 'entries'))
    comments = fields.Nested('CommentSchema', many=True,
                             exclude=('user', 'entry'))
    likes = fields.Nested('LikeSchema', many=True,
                          exclude=('user', 'entry'))


user_schema = UserSchema()
users_schema = UserSchema(many=True)

from main import ma
from marshmallow import fields, validate
from models.diaries import Diary, PrivacyOptions
from schemas.common import TrimmedString


class PrivacyStringField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        try:
            #  Sanitize privacy field
            return PrivacyOptions(str(value).upper())
        except ValueError:
            raise fields.ValidationError(
                "Invalid enum value, must be one of [PUBLIC, PRIVATE]"
            )


class DiarySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Diary
        include_relationships = True

    id = fields.Int(dump_only=True)
    title = TrimmedString(
        required=True, validate=validate.Length(
            min=1, error="Diary Title cannot be empty"
        )
    )  # Sanitize and validate Title
    date_created = fields.DateTime(dump_only=True)
    privacy = PrivacyStringField()
    entries = fields.Nested('EntrySchema', many=True,
                            exclude=('diary', 'comments', 'likes', 'tags'))
    user = fields.Nested('UserSchema',

                         exclude=('diaries', 'comments', 'likes'))


diary_schema = DiarySchema()
diaries_schema = DiarySchema(many=True)

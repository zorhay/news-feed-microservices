from marshmallow import fields, Schema, ValidationError, pre_load

from app.models import User


def unique_user_email(value: str) -> None:
    if User.query.filter_by(email=value.lower()).first():
        raise ValidationError(message="User with given email already exists.")


class SignUpUserSchema(Schema):
    email = fields.String(required=True, allow_none=False, validate=[unique_user_email])
    password = fields.String(required=True, allow_none=False)

    @pre_load
    def _make_lowercase(self, data, **kwargs):
        data["email"] = data["email"].lower()
        return data


class UserMetadataSchema(Schema):
    device = fields.String(required=True)
    country = fields.String(required=True)

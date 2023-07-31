from marshmallow import fields, Schema


class CreateSubscriptionSchema(Schema):
    client_id = fields.Integer(required=True)
    device = fields.String(required=True)
    country = fields.String(required=True)

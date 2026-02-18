from marshmallow import Schema, fields

class UserSchema(Schema):
    """Schema for serializing and deserializing User objects."""
    
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)

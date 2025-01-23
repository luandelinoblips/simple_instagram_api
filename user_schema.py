from marshmallow import Schema, fields


class PostSchema(Schema):
    _id = fields.String(required=True)
    type = fields.String(required=True)
    caption = fields.String()
    media_url = fields.String()
    permalink = fields.String()
    timestamp = fields.String()
    like_count = fields.Integer()
    comments_count = fields.Integer()
    is_video = fields.Boolean()
    has_audio = fields.Boolean()


class UserSchema(Schema):
    _id = fields.String(required=True)
    name = fields.String()
    username = fields.String(required=True)
    img_url = fields.String()
    email = fields.String()
    bio = fields.String()
    followers = fields.Integer()
    following = fields.Integer()
    num_posts = fields.Integer()
    category_name = fields.String()
    posts = fields.List(fields.Nested(PostSchema)) 
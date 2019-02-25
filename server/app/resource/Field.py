from flask_restful import fields

PostField = {
    "id": fields.Integer,
    "title": fields.String,
    "content": fields.String,
    "create_at": fields.DateTime(dt_format='iso8601'),
    "last_update": fields.DateTime(dt_format='iso8601')
}

PostListField = {
    "total_page": fields.String,
    "current_page": fields.String,
    "posts": fields.List(fields.Nested(PostField))
}
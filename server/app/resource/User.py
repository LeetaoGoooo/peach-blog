from flask_restful import Resource,reqparse
from flask import jsonify
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from app.models import User

class UserResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_name',location='form')
        parser.add_argument('password',location='form')
        args = parser.parse_args()
        user_name = args['user_name']
        password = args['password']
        user = User.query.filter_by(user_name=user_name).first()
        if user is None:
            return {"msg":"用户 {} 不存在!".format(user_name)}
        if not user.verify_password(password):
            return {"msg":"密码错误!"}
        access_token = create_access_token(identity=user_name)
        return {"token":access_token}

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {"current_user":current_user}
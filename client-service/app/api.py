from http import HTTPStatus

from flask import request, Blueprint
from flasgger import swag_from

from app.services import get_user_metadata, signup_user
from app.schemas import SignUpUserSchema


api = Blueprint("signup", __name__)


@api.route("/signup", methods=["POST"])
@swag_from("../apidoc/signup.yaml")
def signup():
    user_data = SignUpUserSchema().load(request.json)
    user_metadata = get_user_metadata(request)
    signup_user(user_data, user_metadata)
    return {"message": "User successfully signed up."}, HTTPStatus.CREATED

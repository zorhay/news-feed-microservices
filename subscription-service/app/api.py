from http import HTTPStatus

from flask import request, Blueprint

from app.schemas import CreateSubscriptionSchema
from app.services import subscribe_client


api = Blueprint("subscribe", __name__)


@api.route("/subscribe", methods=["POST"])
def subscribe():
    data = CreateSubscriptionSchema().load(request.json)
    subscribe_client(data)
    return {}, HTTPStatus.CREATED

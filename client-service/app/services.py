import os
from http import HTTPStatus
from wsgiref.headers import Headers

import requests
from requests import Response
from werkzeug.security import generate_password_hash
from flask import Request

from app.errors import UserSignUpError, ServiceUnavailableError
from app.models import User
from app.schemas import SignUpUserSchema
from app.extensions import db


def get_country_from_ip(ip_address: str) -> str:
    url = f"https://ipinfo.io/{ip_address}/country"
    response = requests.get(url)
    if response.status_code == HTTPStatus.OK:
        return response.text.strip().upper()
    else:
        return "Unknown"


def get_device_info(headers: Headers) -> str:
    return headers.get("User-Agent").lower()


def get_user_metadata(request: Request) -> dict:
    return {"device": get_device_info(request.headers),
            "country": get_country_from_ip(request.remote_addr)}


def create_user(user_data: SignUpUserSchema) -> User:
    user = User(email=user_data["email"], password_hash=generate_password_hash(user_data["password"]))
    db.session.add(user)
    db.session.flush()
    db.session.refresh(user)
    return user


def subscribe_user(user_id: int, device: str, country: str) -> Response:
    url = os.environ["SUBSCRIPTION_SERVICE_API"] + "/subscribe"
    try:
        return requests.post(url, json={"client_id": user_id, "device": device, "country": country})
    except requests.exceptions.ConnectionError:
        raise ServiceUnavailableError


def signup_user(user_data: SignUpUserSchema, user_metadata: dict) -> None:
    with db.session.begin_nested():
        user = create_user(user_data)
        result = subscribe_user(user.id, **user_metadata)
        if result.status_code != HTTPStatus.CREATED:
            db.session.rollback()
            raise UserSignUpError(result.text)
        db.session.commit()

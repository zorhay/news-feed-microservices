from unittest import mock

import pytest

from app import create_app, UserSignUpError, ServiceUnavailableError
from app.extensions import db
from app.schemas import SignUpUserSchema
from app.services import get_country_from_ip, signup_user
from app.models import User


@pytest.fixture
def client():
    app = create_app(config_object="app.config.TestingConfig")
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            yield client
            db.session.remove()


@mock.patch("app.services.subscribe_user")
def test_should_successfully_create_user_if_subscribe_is_successful(subscribe_user, client):
    # when
    mock_response = subscribe_user.return_value
    mock_response.status_code = 201

    user_data = SignUpUserSchema().load({
        "email": "test@test.com",
        "password": "test"
    })
    user_metadata = {
        "device": "ios",
        "country": "US"
    }
    # do
    signup_user(user_data, user_metadata)

    # then
    user = User.query.filter_by(email=user_data["email"]).first()
    assert user is not None
    assert user.id is not None


@mock.patch("app.services.subscribe_user")
def test_should_rise_an_exception_if_subscribe_is_fail(subscribe_user, client):
    # when
    mock_response = subscribe_user.return_value
    mock_response.status_code = 500

    user_data = SignUpUserSchema().load({
        "email": "test@test.com",
        "password": "test"
    })
    user_metadata = {
        "device": "ios",
        "country": "US"
    }

    # then
    with pytest.raises(UserSignUpError):
        signup_user(user_data, user_metadata)

    user = User.query.filter_by(email=user_data["email"]).first()
    assert user is None


@mock.patch("app.services.subscribe_user")
def test_should_rollback_user_if_subscription_service_unavailable(subscribe_user, client):
    # when
    subscribe_user.side_effect = ServiceUnavailableError()

    user_data = SignUpUserSchema().load({
        "email": "test@test.com",
        "password": "test"
    })
    user_metadata = {
        "device": "ios",
        "country": "US"
    }

    # then
    with pytest.raises(ServiceUnavailableError):
        signup_user(user_data, user_metadata)

    user = User.query.filter_by(email=user_data["email"]).first()
    assert user is None


def test_should_successfully_get_country_from_ip():
    # when
    ip = "8.8.8.8"
    # do
    country = get_country_from_ip(ip)
    # then
    assert country == "US"


def test_should_response_with_unknown_if_ip_not_found():
    # when
    ip = "8.8.8.888"
    # do
    country = get_country_from_ip(ip)
    # then
    assert country == "Unknown"





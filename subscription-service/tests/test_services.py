from unittest import mock
from unittest.mock import Mock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app import SubscriptionPlanNotFoundError, SubscriptionCreationError, create_app, db
from app.models import Plan
from app.schemas import CreateSubscriptionSchema
from app.services import subscribe_client


@pytest.fixture
def client():
    app = create_app(config_object="app.config.TestingConfig")
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            yield client
            db.session.remove()

def create_test_subscription_plan(price, device, country):
    plan = Plan(name="Test", price=price, device=device, country=country)
    db.session.add(plan)
    db.session.commit()


def test_get_plan(client):
    # when
    create_test_subscription_plan(price=1.99, device="ios", country="US")

    subscription_data = CreateSubscriptionSchema().load({
        "client_id": 1,
        "device": "ios",
        "country": "US"
    })

    # then
    subscribe_client(subscription_data)


def test_should_raise_exception_when_subscription_plan_is_missing(client):
    # when
    subscription_data = CreateSubscriptionSchema().load({
        "client_id": 1,
        "device": "ios",
        "country": "US"
    })

    # then
    with pytest.raises(SubscriptionPlanNotFoundError):
        subscribe_client(subscription_data)


@mock.patch("app.services.db")
def test_should_raise_exception_when_subscription_insertion_fails(db, client):
    # when
    create_test_subscription_plan(price=1.99, device="ios", country="US")
    db.session.commit = Mock(side_effect=SQLAlchemyError())

    subscription_data = CreateSubscriptionSchema().load({
        "client_id": 1,
        "device": "ios",
        "country": "US"
    })

    # then
    with pytest.raises(SubscriptionCreationError):
        subscribe_client(subscription_data)

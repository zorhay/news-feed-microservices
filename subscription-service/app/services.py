from sqlalchemy.exc import SQLAlchemyError

from app.errors import SubscriptionCreationError, SubscriptionPlanNotFoundError
from app.models import Subscription, Plan
from app.schemas import CreateSubscriptionSchema
from app.extensions import db


def get_subscription_plan(country: str, device: str):  # -> Plan
    return Plan.query.filter(Plan.country == country, Plan.device == device).first()


def create_subscription(plan_id: int, client_id: int) -> None:
    subscription = Subscription(plan_id=plan_id, client_id=client_id)
    db.session.add(subscription)
    db.session.commit()


def subscribe_client(data: CreateSubscriptionSchema) -> None:
    plan = get_subscription_plan(country=data["country"], device=data["device"])
    if not plan:
        raise SubscriptionPlanNotFoundError
    try:
        create_subscription(plan_id=plan.id, client_id=data["client_id"])
    except SQLAlchemyError:
        raise SubscriptionCreationError

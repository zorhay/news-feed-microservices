from sqlalchemy import func, ForeignKey

from app.extensions import db


class BaseMixin(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, onupdate=func.now())


class Plan(db.Model, BaseMixin):
    __tablename__ = "plans"
    name = db.Column(db.String, nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    device = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)


class Subscription(db.Model, BaseMixin):
    __tablename__ = "subscriptions"
    plan_id = db.Column(db.Integer, ForeignKey("plans.id", ondelete="CASCADE"), nullable=False)
    plan = db.relationship("Plan")

    client_id = db.Column(db.Integer, nullable=False)

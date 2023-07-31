import dotenv
from flask import Flask

from app.models import db, Plan  # noqa
from app.api import api as api_bp
from app.errors import (subscription_creation_error_handler, SubscriptionCreationError,
                        SubscriptionPlanNotFoundError, plan_not_found_error_handler)


def create_app(config_object="app.config.Config") -> Flask:
    dotenv.load_dotenv()
    app = Flask(__name__)
    app.config.from_object(obj=config_object)

    db.init_app(app)

    # with app.app_context():
    #     db.create_all()
    #     plan1 = Plan(name="Basic", price=1.99, device="ios", country="Unknown")
    #     db.session.add(plan1)
    #     db.session.commit()

    app.register_blueprint(blueprint=api_bp)

    app.register_error_handler(SubscriptionCreationError, subscription_creation_error_handler)
    app.register_error_handler(SubscriptionPlanNotFoundError, plan_not_found_error_handler)

    return app

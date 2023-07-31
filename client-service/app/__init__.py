import dotenv
from flask import Flask
from marshmallow import ValidationError

from app.errors import handle_validation_error, UserSignUpError, handle_user_sign_up_fail_error, \
    ServiceUnavailableError, handle_service_unavailable_error
from app.extensions import swagger
from app.models import db  # noqa
from app.api import api as api_bp


def create_app(config_object="app.config.Config"):
    dotenv.load_dotenv()

    app = Flask(__name__)
    app.config.from_object(obj=config_object)

    db.init_app(app)
    swagger.init_app(app)

    app.register_blueprint(blueprint=api_bp)

    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(UserSignUpError, handle_user_sign_up_fail_error)
    app.register_error_handler(ServiceUnavailableError, handle_service_unavailable_error)

    return app

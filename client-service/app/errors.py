from http import HTTPStatus

from marshmallow import ValidationError


class ApiBaseError(Exception):
    message = "An error occurred"

    def __init__(self, message=None):
        self.message = message or self.message


class UserSignUpError(ApiBaseError):
    message = "Failed to sign up user."


class ServiceUnavailableError(ApiBaseError):
    message = "Service is unavailable."


def handle_validation_error(error: ValidationError):
    return {"errors": error.messages}, HTTPStatus.UNPROCESSABLE_ENTITY


def handle_user_sign_up_fail_error(error: UserSignUpError):
    return {"errors": error.message}, HTTPStatus.UNPROCESSABLE_ENTITY


def handle_service_unavailable_error(error: ServiceUnavailableError):
    return {"errors": error.message}, HTTPStatus.SERVICE_UNAVAILABLE

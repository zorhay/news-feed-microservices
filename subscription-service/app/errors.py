from http import HTTPStatus


class ApiBaseError(Exception):
    message = "An error occurred"

    def __init__(self, message=None):
        self.message = message or self.message


class SubscriptionCreationError(ApiBaseError):
    message = "Subscription creation internal error."


class SubscriptionPlanNotFoundError(ApiBaseError):
    message = "Subscription plan for client can not be found."


def subscription_creation_error_handler(error: SubscriptionCreationError):
    return error.message, HTTPStatus.SERVICE_UNAVAILABLE


def plan_not_found_error_handler(error: SubscriptionPlanNotFoundError):
    return error.message, HTTPStatus.NOT_FOUND

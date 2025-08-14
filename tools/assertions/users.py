from clients.users.users_schema import (
    CreateUserRequestSchema,
    CreateUserResponseSchema,
    UserSchema,
)
from tools.assertions.base import assert_models_match
import allure
from tools.logger import get_logger


logger = get_logger("USERS_ASSERTION")


@allure.step("Check user response.")
def assert_create_user_response(
    request: CreateUserRequestSchema,
    response: CreateUserResponseSchema,
):
    """Compares request data with the user data in the response."""
    logger.info("Check user response.")

    field_to_compare = list(CreateUserRequestSchema.model_fields.keys() - {"password"})
    assert_models_match(response.user, request, field_to_compare)


@allure.step("Check get user response.")
def assert_get_user_response(
    get_user_response: UserSchema,
    create_user_response: CreateUserResponseSchema,
):
    """Asserts that the user from a GET response matches the created user."""
    logger.info("Check get user response.")

    assert_models_match(actual=get_user_response, expected=create_user_response.user)

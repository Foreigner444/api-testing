from assertpy import assert_that
from pytest_check import check
import allure
from clients.auth_client.authentication_schema import LoginResponseSchema
from tools.logger import get_logger


logger = get_logger("LOGIN_ASSERTION")


@allure.step("Check login response.")
def assert_login_response(response: LoginResponseSchema):
    """
    Validates the entire login response, reporting all failures.
    """
    logger.info("Check login response")
    with check:
        assert_that(response.token.token_type).is_equal_to("bearer")
    with check:
        assert_that(response.token.access_token).is_not_none().is_not_empty()
    with check:
        assert_that(response.token.refresh_token).is_not_none().is_not_empty()

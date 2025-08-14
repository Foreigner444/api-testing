from http import HTTPStatus

import allure
import pytest

from clients.auth_client.authentication_client import AuthenticationClient
from clients.auth_client.authentication_schema import (
    LoginRequestSchema,
    LoginResponseSchema,
)
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeatures
from tools.allure.strories import AllureStory
from tools.allure.tags import AllureTags
from tools.assertions.base import assert_status_code
from tools.assertions.login import assert_login_response
from tools.assertions.schema import validate_json_schema
from allure_commons.types import Severity


@pytest.mark.regression
@pytest.mark.authentication
@allure.tag(AllureTags.REGRESSION, AllureTags.AUTHENTICATION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeatures.AUTHENTICATION)
class TestAuthentication:
    @allure.title("Login with valid email and password.")
    @allure.story(AllureStory.LOGIN)
    @allure.severity(Severity.BLOCKER)
    def test_login(
        self, authentication_client: AuthenticationClient, function_user: UserFixture
    ):
        request = LoginRequestSchema(
            email=function_user.email, password=function_user.password
        )
        response = authentication_client.login_api(request)
        response_data = LoginResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_login_response(response_data)
        validate_json_schema(
            instance=response.json(), schema=response_data.model_json_schema()
        )

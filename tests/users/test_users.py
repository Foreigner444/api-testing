from http import HTTPStatus

import allure
import pytest
from faker import Faker

from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import (
    CreateUserRequestSchema,
    CreateUserResponseSchema,
    GetUserResponseSchema,
)
from tests.conftest import UserTestContext
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeatures
from tools.allure.strories import AllureStory
from tools.allure.tags import AllureTags
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response
from allure_commons.types import Severity

fake = Faker()


@pytest.mark.users
@pytest.mark.regression
@allure.tag(AllureTags.USERS, AllureTags.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeatures.USERS)
class TestUsers:
    @pytest.mark.parametrize("domain", ["outlook.com", "gmail.com", "yahoo.com"])
    @allure.title("Create user.")
    @allure.tag(AllureTags.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    def test_create_user(self, domain: str, public_users_client: PublicUsersClient):
        request = CreateUserRequestSchema(email=fake.email(domain=domain))  # noqa
        response = public_users_client.create_user_api(request=request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_user_response(request, response_data)
        validate_json_schema(
            instance=response.json(), schema=response_data.model_json_schema()
        )

    @allure.title("Get current user info.")
    @allure.tag(AllureTags.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.severity(Severity.CRITICAL)
    def test_get_user_me(self, user_context: UserTestContext):
        """
        Test the GET /users/me endpoint for an authenticated user.
        """
        response = user_context.client.get_user_me_api()
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_data.user, user_context.user_data)
        validate_json_schema(
            instance=response.json(), schema=response_data.model_json_schema()
        )

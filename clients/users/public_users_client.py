from httpx import Response
import allure
from clients.api_client import ApiClient
from clients.public_http_builder import get_public_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.routes import APIRoutes


class PublicUsersClient(ApiClient):
    @allure.step("Create user.")
    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        return self.post(url=APIRoutes.USERS, json=request.model_dump(by_alias=True))

    def create_user(self, request: CreateUserRequestSchema) -> CreateUserResponseSchema:
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)


def get_public_users_client() -> PublicUsersClient:
    return PublicUsersClient(client=get_public_client())

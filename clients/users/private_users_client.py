from httpx import Response
from clients.api_client import ApiClient
from clients.private_http_builder import (
    AuthenticationUserSchema,
    get_private_http_client,
)
from clients.users.users_schema import GetUserResponseSchema, UpdateUserRequestSchema
import allure
from tools.routes import APIRoutes



class PrivateUsersClient(ApiClient):
    @allure.step("Get user me.")
    def get_user_me_api(self) -> Response:
        return self.get(url=f"{APIRoutes.USERS}/me")

    @allure.step("Get user by id {user_id}.")
    def get_user_by_id_api(self, user_id: str) -> Response:
        return self.client.get(url=f"{APIRoutes.USERS}/{user_id}")

    @allure.step("Update user by id {user_id}.")
    def update_user_api(
        self, user_id: str, request: UpdateUserRequestSchema
    ) -> Response:
        return self.client.patch(
            url=f"{APIRoutes.USERS}/{user_id}", json=request.model_dump(by_alias=True)
        )

    @allure.step("Delete user by id {user_id}.")
    def delete_user_api(self, user_id: str) -> Response:
        return self.client.delete(url=f"{APIRoutes.USERS}/{user_id}")

    @allure.step("Get user by id {user_id}.")
    def get_user(self, user_id: str) -> GetUserResponseSchema:
        response = self.get(
            url=f"{APIRoutes.USERS}/{user_id}",
        )
        return GetUserResponseSchema.model_validate_json(response.text)


def get_private_users_client(user: AuthenticationUserSchema) -> PrivateUsersClient:
    return PrivateUsersClient(client=get_private_http_client(user=user))

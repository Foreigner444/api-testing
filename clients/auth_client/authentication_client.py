from httpx import Response
import allure
from clients.api_client import ApiClient
from clients.auth_client.authentication_schema import (
    LoginRequestSchema,
    LoginResponseSchema,
    RefreshRequestSchema,
)
from clients.public_http_builder import get_public_client
from tools.routes import APIRoutes


class AuthenticationClient(ApiClient):
    @allure.step("Authenticate user.")
    def login_api(self, request: LoginRequestSchema) -> Response:
        return self.post(
            url=f"{APIRoutes.AUTHENTICATION}/login", json=request.model_dump(by_alias=True)
        )
    @allure.step("Refresh authentication token.")
    def refresh_api(self, request: RefreshRequestSchema) -> Response:
        return self.post(
            url=f"{APIRoutes.AUTHENTICATION}/refresh", json=request.model_dump(by_alias=True)
        )

    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        response = self.login_api(request)
        return LoginResponseSchema.model_validate_json(response.text)

    def refresh(self, request: RefreshRequestSchema) -> LoginResponseSchema:
        response = self.refresh_api(request)
        return LoginResponseSchema.model_validate_json(response.text)


def get_authentication_client() -> AuthenticationClient:
    return AuthenticationClient(client=get_public_client())

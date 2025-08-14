import pytest
from pydantic import BaseModel, EmailStr

from clients.authenticated_api_client import AuthenticatedApiClient
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient, get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema


class UserFixture(BaseModel):
    request: CreateUserRequestSchema
    response: CreateUserResponseSchema

    @property
    def user_id(self):
        return self.response.user.id

    @property
    def authentication_user(self) -> AuthenticationUserSchema:
        return AuthenticationUserSchema(
            email=self.request.email, password=self.request.password
        )

    @property
    def email(self) -> EmailStr:
        return self.request.email

    @property
    def password(self) -> str:
        return self.request.password


@pytest.fixture
def public_users_client() -> PublicUsersClient:
    return get_public_users_client()


@pytest.fixture
def function_user(public_users_client: PublicUsersClient) -> UserFixture:
    request = CreateUserRequestSchema()
    response = public_users_client.create_user(request)
    return UserFixture(request=request, response=response)


@pytest.fixture
def private_user_client(
    function_user: UserFixture.authentication_user,
) -> PrivateUsersClient:
    return AuthenticatedApiClient(function_user).users

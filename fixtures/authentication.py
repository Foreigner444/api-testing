import pytest

from clients.auth_client.authentication_client import (
    AuthenticationClient,
    get_authentication_client,
)


@pytest.fixture
def authentication_client() -> AuthenticationClient:
    return get_authentication_client()

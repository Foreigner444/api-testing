import pytest

from clients.files.files_client import PrivateFilesClient, get_private_files_client
from clients.users.private_users_client import (
    PrivateUsersClient,
    get_private_users_client,
)
from fixtures.files import FileFixture
from fixtures.users import UserFixture


class UserTestContext:
    def __init__(self, user_fixture: UserFixture):
        self.user_fixture = user_fixture
        self.client: PrivateUsersClient = get_private_users_client(
            user_fixture.authentication_user
        )

    @property
    def user_data(self):
        return self.user_fixture.response


@pytest.fixture(scope="function")
def user_context(function_user: UserFixture):
    return UserTestContext(user_fixture=function_user)


class FileTestContext:
    def __init__(self, user_fixture: UserFixture, file_fixture: FileFixture):
        self.file_fixture = file_fixture
        self.client: PrivateFilesClient = get_private_files_client(
            user_fixture.authentication_user
        )

    @property
    def file_data(self):
        return self.file_fixture.response


@pytest.fixture(scope="function")
def file_context(function_user: UserFixture, function_file: FileFixture):
    return FileTestContext(user_fixture=function_user, file_fixture=function_file)

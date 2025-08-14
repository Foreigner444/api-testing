import pytest
from pydantic import BaseModel

from clients.files.files_client import PrivateFilesClient, get_private_files_client
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from fixtures.users import UserFixture


class FileFixture(BaseModel):
    request: CreateFileRequestSchema
    response: CreateFileResponseSchema

    @property
    def file_id(self):
        return self.response.file.id


@pytest.fixture
def files_client(function_user: UserFixture) -> PrivateFilesClient:
    return get_private_files_client(function_user.authentication_user)


@pytest.fixture
def function_file(files_client: PrivateFilesClient) -> FileFixture:
    request = CreateFileRequestSchema(upload_file="./testdata/files/test.svg")
    response = files_client.create_file(request)
    return FileFixture(request=request, response=response)

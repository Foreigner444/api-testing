import uuid
import allure
from httpx import Response
from tools.routes import APIRoutes
from clients.api_client import ApiClient
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from clients.private_http_builder import (
    AuthenticationUserSchema,
    get_private_http_client,
)


class PrivateFilesClient(ApiClient):
    @allure.step("Get file by id {file_id}.")
    def get_file_by_id_api(self, file_id: str) -> Response:
        return self.get(url=f"{APIRoutes.FILES}/{file_id}")

    @allure.step("Create file.")
    def create_file_api(self, request: CreateFileRequestSchema):
        return self.post(
            url=APIRoutes.FILES,
            data=request.model_dump(by_alias=True, exclude={"upload_file"}),
            files={"upload_file": request.upload_file.read_bytes()},
        )

    @allure.step("Delete file by id {file_id}.")
    def delete_file_by_id_api(self, file_id: uuid.UUID) -> Response:
        return self.delete(url=f"{APIRoutes.FILES}/{file_id}")

    @allure.step("Create file.")
    def create_file(self, request: CreateFileRequestSchema) -> CreateFileResponseSchema:
        response = self.post(
            url=APIRoutes.FILES,
            data=request.model_dump(by_alias=True, exclude={"upload_file"}),
            files={"upload_file": open(request.upload_file, "rb")},
        )
        return CreateFileResponseSchema.model_validate_json(response.text)


def get_private_files_client(user: AuthenticationUserSchema) -> PrivateFilesClient:
    return PrivateFilesClient(client=get_private_http_client(user=user))

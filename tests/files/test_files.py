from http import HTTPStatus
from config import settings
import allure
import pytest

from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
)
from clients.files.files_schema import (
    CreateFileRequestSchema,
    CreateFileResponseSchema,
    GetFileResponseSchema,
)
from tests.conftest import FileTestContext
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeatures
from tools.allure.strories import AllureStory
from tools.allure.tags import AllureTags
from tools.assertions.base import assert_status_code
from tools.assertions.error import assert_validation_error_for_field
from tools.assertions.files import (
    assert_create_file_response,
    assert_file_not_found_response,
    assert_get_file_response,
)
from tools.assertions.schema import validate_json_schema
from allure_commons.types import Severity


@pytest.mark.files
@pytest.mark.regression
@allure.tag(AllureTags.FILES, AllureTags.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeatures.FILES)
class TestFiles:
    @allure.title("Create file.")
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    def test_create_file(self, file_context: FileTestContext):
        request = CreateFileRequestSchema(upload_file=settings.test_data.img_png_file)
        response = file_context.client.create_file_api(request=request)
        response_data = CreateFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_file_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title("Get file.")
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.tag(AllureTags.GET_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    def test_get_file(self, file_context: FileTestContext):
        response = file_context.client.get_file_by_id_api(
            file_context.file_data.file.id
        )
        response_data = GetFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_file_response(response_data, file_context.file_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title("Get file with empty filename.")
    @allure.tag(AllureTags.VALIDATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_file_with_empty_filename(self, file_context: FileTestContext):
        request = CreateFileRequestSchema(
            upload_file=settings.test_data.img_png_file, filename=""
        )
        response = file_context.client.create_file_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        assert_status_code(
            response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY, response.json()
        )
        with allure.step("Check file with empty filename response."):
            assert_validation_error_for_field(
                response_data,
                field_name="filename",
                error_type="string_too_short",
                input_value="",
                context={"min_length": 1},
                message="String should have at least 1 character",
            )
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title("Get file with empty directory.")
    @allure.tag(AllureTags.VALIDATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_file_with_empty_directory(self, file_context: FileTestContext):
        request = CreateFileRequestSchema(
            upload_file=settings.test_data.img_png_file, directory=""
        )
        response = file_context.client.create_file_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        assert_status_code(
            response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY, response.json()
        )
        with allure.step("Check create file with empty directory response."):
            assert_validation_error_for_field(
                response_data,
                field_name="directory",
                error_type="string_too_short",
                input_value="",
                context={"min_length": 1},
                message="String should have at least 1 character",
            )
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title("Delete file.")
    @allure.tag(AllureTags.DELETE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_delete_file(self, file_context: FileTestContext):
        response = file_context.client.delete_file_by_id_api(
            file_context.file_data.file.id
        )
        assert_status_code(response.status_code, HTTPStatus.OK)

        get_response = file_context.client.get_file_by_id_api(
            file_context.file_data.file.id
        )
        get_response_data = InternalErrorResponseSchema.model_validate_json(
            get_response.text
        )
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        assert_file_not_found_response(get_response_data)

        validate_json_schema(get_response.json(), get_response_data.model_json_schema())

    @allure.title("Get file with with invalid file id.")
    @allure.tag(AllureTags.VALIDATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    def test_get_file_with_incorrect_file_id(self, file_context: FileTestContext):
        invalid_uuid = "incorrect_file_id"
        response = file_context.client.get_file_by_id_api(invalid_uuid)

        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        assert_status_code(
            response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY, response.json()
        )
        with allure.step("Check get file with invalid file id response."):
            assert_validation_error_for_field(
                response_data,
                field_name="file_id",
                error_type="uuid_parsing",
                input_value=invalid_uuid,
                context={
                    "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"
                },
                message="Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1",
            )

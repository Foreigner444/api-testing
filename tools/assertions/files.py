from http import HTTPStatus
import allure
import httpx

from clients.errors_schema import InternalErrorResponseSchema
from clients.files.files_schema import (
    CreateFileRequestSchema,
    CreateFileResponseSchema,
    FileSchema,
    GetFileResponseSchema,
)
from tools.assertions.base import assert_models_match, assert_status_code
from tools.assertions.error import assert_internal_error_response
from tools.logger import get_logger


logger = get_logger("FILES_ASSERTION")

@allure.step("Verify that file exists.")
def assert_file_exists(url: str):

    logger.info("Verify that file exists.")

    response = httpx.get(url=url)
    assert_status_code(response.status_code, HTTPStatus.OK)


@allure.step("Check create file response.")
def assert_create_file_response(
    request: CreateFileRequestSchema, response: CreateFileResponseSchema
):
    logger.info("Check create file response.")

    fields_to_compare = ["filename", "directory"]
    assert_models_match(request, response.file, fields_to_compare)
    assert_file_exists(str(response.file.url))


@allure.step("Check file.")
def assert_file(
    actual: FileSchema,
    expected: FileSchema,
):
    """
    Dynamically compares fields of two FileSchema models
    """
    logger.info("Check file.")
    fields_to_check = expected.model_fields.keys()

    assert_models_match(actual, expected, fields_to_check)


@allure.step("Check get file response.")
def assert_get_file_response(
    get_file_response: GetFileResponseSchema,
    create_file_response: CreateFileResponseSchema,
):
    logger.info("Check get file response.")

    assert_file(get_file_response.file, create_file_response.file)


@allure.step("Check file not found response.")
def assert_file_not_found_response(actual: InternalErrorResponseSchema):

    logger.info("Check file not found response.")

    expected = InternalErrorResponseSchema(detail="File not found")
    assert_internal_error_response(actual, expected)

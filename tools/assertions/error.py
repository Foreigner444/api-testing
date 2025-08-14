from typing import Any
import allure
from pydantic import BaseModel

from clients.errors_schema import ValidationErrorResponseSchema, ValidationErrorSchema
from tools.assertions.base import assert_length
from tools.logger import get_logger


logger = get_logger("ERRORS_ASSERTION")


@allure.step("Check validation error.")
def assert_validation_error(actual: BaseModel, expected: BaseModel):
    """
    Asserts that two ValidationErrorSchema objects are equal.
    Pydantic models are compared field by field by default.
    """
    logger.info("Verify validation error")
    assert actual == expected, (
        f"\n{'=' * 20} VALIDATION ERROR MISMATCH {'=' * 20}\n"
        f"  - Expected: {expected.model_dump_json(indent=2)}\n"
        f"  - Actual:   {actual.model_dump_json(indent=2)}\n"
        f"{'=' * 58}"
    )

@allure.step("Check validation error response.")
def assert_validation_error_response(
    actual: ValidationErrorResponseSchema, expected: ValidationErrorResponseSchema
):
    """
    Asserts that the validation error responses are equivalent,
    regardless of the order of errors in the 'details' list.
    """
    logger.info("Verify validation error response")
    assert_length(actual=actual.details, expected=expected.details, name="details")

    sorted_actual_details = sorted(
        actual.details, key=lambda d: tuple(map(str, d.location))
    )
    sorted_expected_details = sorted(
        expected.details, key=lambda d: tuple(map(str, d.location))
    )

    for actual_details, expected_details in zip(
        sorted_actual_details, sorted_expected_details
    ):
        assert_validation_error(actual_details, expected_details)


def build_expected_validation_error(
    field_name: str,
    error_type: str,
    input_value: Any,
    context: dict = None,
    message: str = None,
) -> ValidationErrorResponseSchema:
    """Helper to build an expected validation error response."""
    logger.info("Building expected validation error response")

    error_details = ValidationErrorSchema(
        type=error_type,
        input=input_value,
        ctx=context,
        msg=message,
        loc=["path" if field_name == "file_id" else "body", field_name],
    )
    return ValidationErrorResponseSchema(detail=[error_details])

@allure.step("Check validation error for field")
def assert_validation_error_for_field(
    actual: ValidationErrorResponseSchema,
    field_name: str,
    error_type: str,
    input_value: Any = None,
    context: dict = None,
    message: str = None,
):
    logger.info(
        f"Validating error for field '{field_name}'. "
        f"Type: {error_type}, Input: {input_value}"
    )
    
    with allure.step(f"Build expected validation error for field '{field_name}'"):
        expected = build_expected_validation_error(
            field_name=field_name,
            error_type=error_type,
            context=context,
            input_value=input_value,
            message=message,
        )
    
    with allure.step("Verify validation error response matches expected"):
        logger.debug(f"Expected error: {expected.model_dump_json(indent=2)}")
        logger.debug(f"Actual error: {actual.model_dump_json(indent=2)}")
        assert_validation_error_response(actual, expected)
        logger.info("Validation error matches expected")


@allure.step("Check internal error response.")
def assert_internal_error_response(actual, expected):
    assert_validation_error(actual.details, expected.details)

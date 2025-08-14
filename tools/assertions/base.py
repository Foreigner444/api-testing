import json
from typing import Any, Sized
import allure
from pydantic import BaseModel
from tools.logger import get_logger


logger = get_logger("BASE_ASSERTIONS")


@allure.step("Check that response status code equal to {expected}.")
def assert_status_code(actual: int, expected: int, response_body: dict = None):
    """Asserts the HTTP status code, with an enhanced error message."""

    logger.info(f"Check that response status code equal to '{expected}'.")

    assert actual == expected, (
        f"\n{'=' * 20} STATUS CODE MISMATCH {'=' * 20}\n"
        f"  - Expected: {expected}\n"
        f"  - Actual:   {actual}\n"
        f"  - Response body:  {
            json.dumps(response_body, indent=2) if response_body else 'N/A'
        }\n"
        f"{'=' * 58}"
    )


@allure.step("Check that {field_name} field value equals to {expected}.")
def assert_equality(actual: Any, expected: Any, field_name: str):
    """Asserts equality with a detailed and formatted error message."""
    logger.info(f"Check that '{field_name}' field value equals to '{expected}'.")

    assert actual == expected, (
        f"\n{'=' * 20} FIELD VALUE MISMATCH: '{field_name}' {'=' * 20}\n"
        f"  - Expected: {repr(expected)}\n"
        f"  - Actual:   {repr(actual)}\n"
        f"{'=' * (58 + len(field_name))}"
    )


@allure.step("Check that {field_name} field value is true.")
def assert_is_true(actual: Any, field_name: str):
    """Asserts that a value is truthy, with an enhanced error message."""
    logger.info(f"Check that '{field_name}' field value is true.")

    assert bool(actual), (
        f"\n{'=' * 20} TRUTHY CHECK FAILED: '{field_name}' {'=' * 20}\n"
        f"  - Expected a truthy value (e.g., not None, not False, not empty).\n"
        f"  - Actual:   {repr(actual)}\n"
        f"{'=' * (55 + len(field_name))}"
    )


def assert_length(actual: Sized, expected: Sized, name: str):
    with allure.step(f"Check that length of {name} equals to {len(expected)}."):
        logger.info(f"Check that length of '{name}' equals to '{len(expected)}'.")

        assert len(actual) == len(expected), (
            f"Incorrect object length: {name}. "
            f"Expected length: {len(expected)}. "
            f"Actual length: {len(actual)}"
    )


def assert_models_match(
    actual: BaseModel, expected: BaseModel, fields_to_check: list[str] = None
):
    """
    Asserts that specified fields are equal between two Pydantic models.
    
    Args:
        actual: The actual model instance to check
        expected: The expected model instance containing the expected values
        fields_to_check: List of field names to compare. If None, all fields are checked.
    """
    if fields_to_check is None:
        fields_to_check = list(expected.model_fields.keys())
    
    fields_str = ', '.join(fields_to_check) if fields_to_check else 'all'
    step_name = f"Verify that model '{actual.__class__.__name__}' matches expected values for fields: {fields_str}"
    
    with allure.step(step_name):
        logger.info(step_name)

        for field in fields_to_check:
            with allure.step(f"Checking field: {field}"):
                logger.info(f"Checking field: {field}")
                assert_equality(
                    getattr(actual, field), 
                    getattr(expected, field), 
                    f"'{field}'"
                )

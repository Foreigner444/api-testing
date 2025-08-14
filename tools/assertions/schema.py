from typing import Any
from jsonschema import validate
from jsonschema.validators import Draft202012Validator
import allure
from tools.logger import get_logger


logger = get_logger("SCHEMA_ASSERTION")


@allure.step("Validate JSON schema.")
def validate_json_schema(instance: Any, schema: dict) -> None:
    logger.info("Validating JSON schema.")
    validate(
        instance=instance,
        schema=schema,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )

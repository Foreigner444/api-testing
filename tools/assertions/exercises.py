from http import HTTPStatus
import allure
from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_api_client import PrivateExercisesClient
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    ExerciseSchema,
    GetExerciseResponseSchema,
    GetExercisesResponseSchema,
    UpdateExerciseRequestSchema,
    UpdateExerciseResponseSchema,
)
from tools.assertions.base import (
    assert_equality,
    assert_length,
    assert_models_match,
    assert_status_code,
)
from tools.assertions.error import assert_internal_error_response
from tools.logger import get_logger


logger = get_logger("EXERCISE_ASSERTIONS")


@allure.step("Create exercise.")
def assert_create_exercise_response(
    request: CreateExerciseRequestSchema, response: CreateExerciseResponseSchema
):
    logger.info("Create exercise")
    fields_to_check = list(request.model_dump(exclude_unset=True).keys())

    assert_models_match(request, response.exercise, fields_to_check)

    assert_equality(
        actual=response.exercise.course_id,
        expected=request.course_id,
        field_name="course_id",
    )


@allure.step("Verify exercise.")
def assert_exercise(request: ExerciseSchema, response: ExerciseSchema):

    logger.info("Verify exercise")

    fields_to_check = list(request.model_dump(exclude_unset=True).keys())

    assert_models_match(request, response, fields_to_check)


@allure.step("Verify get exercise response.")
def assert_get_exercise_response(
    get_exercise_response: GetExerciseResponseSchema,
    create_exercise_response: CreateExerciseResponseSchema,
):
    logger.info("Verify get exercise response")

    assert_exercise(get_exercise_response.exercise, create_exercise_response.exercise)


@allure.step("Update exercise.")
def assert_update_exercise_response(
    request: UpdateExerciseRequestSchema, response: UpdateExerciseResponseSchema
):
    logger.info("Update exercise")
    fields_to_check = list(request.model_dump(exclude_unset=True).keys())

    assert_models_match(request, response.exercise, fields_to_check)


@allure.step("Verify exercise is updated.")
def assert_exercise_is_updated(
    client: PrivateExercisesClient,
    exercise_id: str,
    request: UpdateExerciseRequestSchema,
):
    logger.info("Verify exercise updated")
    get_exercise_response = client.get_exercise_api(exercise_id)
    get_exercise_response_data = GetExerciseResponseSchema.model_validate_json(
        get_exercise_response.text
    )

    assert_status_code(get_exercise_response.status_code, HTTPStatus.OK)

    assert get_exercise_response_data.exercise.title == request.title


@allure.step("Verify exercise not found response.")
def assert_exercise_not_found_response(actual: InternalErrorResponseSchema):

    logger.info("Verify exercise not found response.")

    expected = InternalErrorResponseSchema(detail="Exercise not found")
    assert_internal_error_response(actual, expected)


@allure.step("Verify of get exercises response.")
def assert_get_exercises_response(
    actual: GetExercisesResponseSchema, expected: list[ExerciseSchema]
):
    logger.info("Verify of get exercises response")
    
    with allure.step(f"Verify number of exercises (expected: {len(expected)})"):
        logger.info(f"Verifying number of exercises. Expected: {len(expected)}")
        assert_length(actual.exercises, expected, "exercises")

    sorted_actual = sorted(actual.exercises, key=lambda exercise: exercise.id)
    sorted_expected = sorted(expected, key=lambda exercise: exercise.id)
    
    with allure.step("Verify each exercise matches expected values"):
        logger.info(f"Verifying {len(sorted_actual)} exercises")
        for i, (actual_exercise, expected_exercise) in enumerate(zip(sorted_actual, sorted_expected), 1):
            with allure.step(f"Verifying exercise {i}/{len(sorted_actual)} (ID: {actual_exercise.id})"):
                logger.info(f"Verifying exercise {i}: ID {actual_exercise.id}")
                assert_models_match(actual_exercise, expected_exercise)


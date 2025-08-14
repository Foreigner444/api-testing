from http import HTTPStatus

import allure
import pytest

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_api_client import PrivateExercisesClient
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExerciseQuerySchema,
    GetExerciseResponseSchema,
    GetExercisesResponseSchema,
    UpdateExerciseRequestSchema,
    UpdateExerciseResponseSchema,
)
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeatures
from tools.allure.strories import AllureStory
from tools.allure.tags import AllureTags
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import (
    assert_create_exercise_response,
    assert_exercise_is_updated,
    assert_exercise_not_found_response,
    assert_get_exercise_response,
    assert_get_exercises_response,
    assert_update_exercise_response,
)
from tools.assertions.schema import validate_json_schema
from allure_commons.types import Severity


@pytest.mark.regression
@pytest.mark.exercises
@allure.tag(AllureTags.REGRESSION, AllureTags.EXERCISES)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeatures.EXERCISES)
class TestExercises:
    @allure.title("Create exercise.")
    @allure.tag(AllureTags.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    def test_create_exercise(
        self, exercises_client: PrivateExercisesClient, function_course: CourseFixture
    ):
        request = CreateExerciseRequestSchema(
            course_id=function_course.course_id  # noqa
        )
        response = exercises_client.create_exercise_api(request)
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_create_exercise_response(request, response_data)
        validate_json_schema(
            response.json(), CreateExerciseResponseSchema.model_json_schema()
        )

    @allure.title("Get exercise.")
    @allure.tag(AllureTags.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.severity(Severity.BLOCKER)
    def test_get_exercise(
        self,
        exercises_client: PrivateExercisesClient,
        function_exercise: ExerciseFixture,
    ):
        response = exercises_client.get_exercise_api(function_exercise.exercise_id)
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_get_exercise_response(response_data, function_exercise.response)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title("Update exercise.")
    @allure.tag(AllureTags.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    def test_update_exercise(
        self,
        exercises_client: PrivateExercisesClient,
        function_exercise: ExerciseFixture,
    ):
        request = UpdateExerciseRequestSchema(title="Updated exercise title")
        response = exercises_client.update_exercise_api(
            function_exercise.exercise_id, request
        )
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_exercise_response(request, response_data)

        validate_json_schema(
            response.json(), UpdateExerciseResponseSchema.model_json_schema()
        )

        assert_exercise_is_updated(exercises_client, response_data.exercise.id, request)

    @allure.title("Delete exercise.")
    @allure.tag(AllureTags.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    def test_delete_exercise(
        self,
        exercises_client: PrivateExercisesClient,
        function_exercise: ExerciseFixture,
    ):
        response = exercises_client.delete_exercise_api(function_exercise.exercise_id)

        assert_status_code(response.status_code, HTTPStatus.OK)

        get_exercise_response = exercises_client.get_exercise_api(
            function_exercise.exercise_id
        )
        get_exercise_response_data = InternalErrorResponseSchema.model_validate_json(
            get_exercise_response.text
        )

        assert_status_code(get_exercise_response.status_code, HTTPStatus.NOT_FOUND)
        assert_exercise_not_found_response(get_exercise_response_data)

        validate_json_schema(
            get_exercise_response.json(), get_exercise_response_data.model_json_schema()
        )

    @allure.title("Get a list of exercises for the course")
    @allure.tag(AllureTags.GET_ENTITIES)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.severity(Severity.BLOCKER)
    def test_get_exercises(
        self,
        exercises_client: PrivateExercisesClient,
        function_exercise: ExerciseFixture,
    ):
        query = GetExerciseQuerySchema(course_id=function_exercise.course_id)  # noqa
        response = exercises_client.get_exercises_api(query)
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        expected_exercises = [function_exercise.exercise]
        assert_get_exercises_response(response_data, expected_exercises)
        validate_json_schema(response.json(), response_data.model_json_schema())

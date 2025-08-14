from http import HTTPStatus

import allure
import pytest

from clients.courses.courses_api_client import PrivateCoursesClient
from clients.courses.courses_schema import (
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
    GetCoursesQuerySchema,
    GetCoursesResponseSchema,
    UpdateCourseRequestSchema,
    UpdateCourseResponseSchema,
)
from fixtures.courses import CourseFixture
from fixtures.files import FileFixture
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeatures
from tools.allure.strories import AllureStory
from tools.allure.tags import AllureTags
from tools.assertions.base import assert_status_code
from tools.assertions.courses import (
    assert_create_course_response,
    assert_get_courses_response,
    assert_update_course_response,
)
from tools.assertions.schema import validate_json_schema
from allure_commons.types import Severity


@pytest.mark.courses
@pytest.mark.regression
@allure.tag(AllureTags.REGRESSION, AllureTags.COURSES)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeatures.COURSES)
class TestCourses:
    @allure.title("Create course.")
    @allure.tag(AllureTags.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    def test_create_course(
        self,
        function_user: UserFixture,
        courses_client: PrivateCoursesClient,
        function_file: FileFixture,
    ):
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.file_id,  # noqa
            created_by_user_id=function_user.user_id,  # noqa
        )
        response = courses_client.create_course_api(request)
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_course_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title("Get course.")
    @allure.tag(AllureTags.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.severity(Severity.BLOCKER)
    def test_get_courses(
        self,
        courses_client: PrivateCoursesClient,
        function_course: CourseFixture,
        function_user: UserFixture,
    ):
        query = GetCoursesQuerySchema(user_id=function_user.user_id)  # noqa
        response = courses_client.get_courses_api(query)
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        expected_courses = [function_course.course]
        assert_get_courses_response(response_data, expected_courses)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title("Update course.")
    @allure.tag(AllureTags.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    def test_update_course(
        self, courses_client: PrivateCoursesClient, function_course: CourseFixture
    ):
        request = UpdateCourseRequestSchema()
        response = courses_client.update_course_api(function_course.course_id, request)

        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)

        assert_update_course_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

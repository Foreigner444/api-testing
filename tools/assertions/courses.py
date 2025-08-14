from clients.courses.courses_schema import (
    CourseSchema,
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
    GetCoursesResponseSchema,
    UpdateCourseRequestSchema,
    UpdateCourseResponseSchema,
)
from tools.assertions.base import assert_equality, assert_length, assert_models_match
import allure
from tools.logger import get_logger


logger = get_logger('COURSES_ASSERTION')


@allure.step("Check create course response.")
def assert_create_course_response(
    request: CreateCourseRequestSchema, response: CreateCourseResponseSchema
):
    logger.info("Check create course response")

    fields_to_exclude = {"created_by_user_id", "preview_file_id"}
    fields_to_check = list(
        CreateCourseRequestSchema.model_fields.keys() - fields_to_exclude
    )

    assert_models_match(request, response.course, fields_to_check)

    assert_equality(
        actual=response.course.created_by_user_id.id,
        expected=request.created_by_user_id,
        field_name="created_by_user_id",
    )

    assert_equality(
        actual=response.course.preview_file.id,
        expected=request.preview_file_id,
        field_name="preview_file_id",
    )


@allure.step("Check update course response.")
def assert_update_course_response(
    request: UpdateCourseRequestSchema, response: UpdateCourseResponseSchema
):
    logger.info("Verify update courses response")

    fields_to_exclude = {"created_by_user_id", "preview_file_id"}
    fields_to_check = list(
        UpdateCourseRequestSchema.model_fields.keys() - fields_to_exclude
    )
    assert_models_match(request, response.course, fields_to_check)


@allure.step("Check get courses response.")
def assert_get_courses_response(
    actual: GetCoursesResponseSchema, expected: list[CourseSchema]
):
    logger.info("Verify get courses response")

    assert_length(actual.courses, expected, "courses")

    sorted_actual = sorted(actual.courses, key=lambda course: course.id)
    sorted_expected = sorted(expected, key=lambda course: course.id)

    for actual_course, expected_course in zip(sorted_actual, sorted_expected):
        assert_models_match(actual_course, expected_course)

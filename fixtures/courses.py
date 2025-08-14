import pytest
from pydantic import BaseModel

from clients.courses.courses_api_client import (
    PrivateCoursesClient,
    get_private_courses_client,
)
from clients.courses.courses_schema import (
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
)
from fixtures.files import FileFixture
from fixtures.users import UserFixture


class CourseFixture(BaseModel):
    request: CreateCourseRequestSchema
    response: CreateCourseResponseSchema

    @property
    def course_id(self):
        return self.response.course.id

    @property
    def course(self):
        return self.response.course


@pytest.fixture
def courses_client(function_user: UserFixture) -> PrivateCoursesClient:
    return get_private_courses_client(function_user.authentication_user)


@pytest.fixture
def function_course(
    courses_client: PrivateCoursesClient,
    function_user: UserFixture,
    function_file: FileFixture,
) -> CourseFixture:
    request = CreateCourseRequestSchema(
        preview_file_id=function_file.file_id, created_by_user_id=function_user.user_id
    )
    response = courses_client.create_course(request)
    return CourseFixture(request=request, response=response)

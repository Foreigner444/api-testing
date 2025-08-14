import uuid
import allure
from httpx import Response

from clients.api_client import ApiClient
from clients.courses.courses_schema import (
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
    GetCoursesQuerySchema,
    UpdateCourseRequestSchema,
)
from clients.private_http_builder import (
    AuthenticationUserSchema,
    get_private_http_client,
)
from tools.routes import APIRoutes


class PrivateCoursesClient(ApiClient):
    @allure.step("Get courses.")
    def get_courses_api(self, query: GetCoursesQuerySchema) -> Response:
        return self.get(url=APIRoutes.COURSES, params=query.model_dump(by_alias=True))

    @allure.step("Get course by id {course_id}.")
    def get_course_by_id_api(self, course_id: uuid.UUID) -> Response:
        return self.get(url=f"{APIRoutes.COURSES}/{course_id}")

    @allure.step("Create course.")
    def create_course_api(self, request: CreateCourseRequestSchema) -> Response:
        return self.post(url=APIRoutes.COURSES, json=request.model_dump(by_alias=True))

    @allure.step("Update course by id {course_id}.")
    def update_course_api(
        self, course_id: str, request: UpdateCourseRequestSchema
    ) -> Response:
        return self.patch(
            url=f"{APIRoutes.COURSES}/{course_id}", json=request.model_dump(by_alias=True)
        )
    @allure.step("Delete course by id {course_id}.")
    def delete_course(self, course_id: str) -> Response:
        return self.delete(url=f"{APIRoutes.COURSES}/{course_id}")

    def create_course(
        self, request: CreateCourseRequestSchema
    ) -> CreateCourseResponseSchema:
        response = self.post(
            url=APIRoutes.COURSES, json=request.model_dump(by_alias=True)
        )
        return CreateCourseResponseSchema.model_validate_json(response.text)


def get_private_courses_client(user: AuthenticationUserSchema) -> PrivateCoursesClient:
    return PrivateCoursesClient(client=get_private_http_client(user=user))

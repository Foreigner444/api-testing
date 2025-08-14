from httpx import Response
import allure
from clients.api_client import ApiClient
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExerciseQuerySchema,
    GetExercisesResponseSchema,
    UpdateExerciseRequestSchema,
)
from clients.private_http_builder import (
    AuthenticationUserSchema,
    get_private_http_client,
)
from tools.routes import APIRoutes


class PrivateExercisesClient(ApiClient):
    @allure.step("Get exercises by course id {query}.")
    def get_exercises_api(self, query: GetExerciseQuerySchema) -> Response:
        return self.get(
            url=APIRoutes.EXERCISES,
            params=query.model_dump(by_alias=True, exclude_none=True),
        )
    @allure.step("Get exercise by id {exercise_id}.")
    def get_exercise_api(self, exercise_id: str) -> Response:
        return self.get(url=f"{APIRoutes.EXERCISES}/{exercise_id}")

    @allure.step("Create exercise.")
    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        return self.post(
            url=APIRoutes.EXERCISES, json=request.model_dump(by_alias=True)
        )

    @allure.step("Update exercise by id {exercise_id}.")
    def update_exercise_api(
        self, exercise_id: str, request: UpdateExerciseRequestSchema
    ) -> Response:
        return self.patch(
            url=f"{APIRoutes.EXERCISES}/{exercise_id}",
            json=request.model_dump(by_alias=True),
        )

    @allure.step("Delete exercise by id {exercise_id}.")
    def delete_exercise_api(self, exercise_id: str) -> Response:
        return self.delete(url=f"{APIRoutes.EXERCISES}/{exercise_id}")

    def create_exercise(
        self, request: CreateExerciseRequestSchema
    ) -> CreateExerciseResponseSchema:
        response = self.post(
            APIRoutes.EXERCISES, json=request.model_dump(by_alias=True)
        )
        return CreateExerciseResponseSchema.model_validate_json(response.text)

    def get_exercises(self, exercise_id: str) -> GetExercisesResponseSchema:
        response = self.get_exercise_api(exercise_id)
        return GetExercisesResponseSchema.model_validate_json(response.text)


def get_private_exercises_client(
    user: AuthenticationUserSchema,
) -> PrivateExercisesClient:
    return PrivateExercisesClient(client=get_private_http_client(user=user))

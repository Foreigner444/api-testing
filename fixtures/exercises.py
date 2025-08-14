import pytest
from pydantic import BaseModel

from clients.exercises.exercises_api_client import (
    PrivateExercisesClient,
    get_private_exercises_client,
)
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
)
from fixtures.users import UserFixture


class ExerciseFixture(BaseModel):
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema

    @property
    def exercise_id(self):
        return self.response.exercise.id

    @property
    def exercise(self):
        return self.response.exercise

    @property
    def course_id(self):
        return self.response.exercise.course_id


@pytest.fixture
def exercises_client(function_user: UserFixture) -> PrivateExercisesClient:
    return get_private_exercises_client(function_user.authentication_user)


@pytest.fixture
def function_exercise(exercises_client: PrivateExercisesClient) -> ExerciseFixture:
    request = CreateExerciseRequestSchema()
    response = exercises_client.create_exercise(request=request)
    return ExerciseFixture(request=request, response=response)

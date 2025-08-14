from pydantic import BaseModel, ConfigDict, Field

from tools.fakers import fake


class ExerciseBase(BaseModel):
    title: str = Field(default_factory=fake.sentence)
    max_score: int = Field(alias="maxScore", default_factory=fake.max_score)
    min_score: int = Field(alias="minScore", default_factory=fake.min_score)
    order_index: int = Field(alias="orderIndex", default_factory=fake.random_number)
    description: str = Field(default_factory=fake.text)
    estimated_time: str = Field(
        alias="estimatedTime", default_factory=fake.estimated_time
    )

    model_config = ConfigDict(populate_by_name=True)


class ExerciseSchema(ExerciseBase):
    id: str
    course_id: str = Field(alias="courseId")


class CreateExerciseRequestSchema(ExerciseBase):
    course_id: str = Field(alias="courseId", default_factory=fake.uuid4)


class CreateExerciseResponseSchema(BaseModel):
    exercise: ExerciseSchema


class GetExerciseResponseSchema(BaseModel):
    exercise: ExerciseSchema


class GetExercisesResponseSchema(BaseModel):
    exercises: list[ExerciseSchema]


class GetExerciseQuerySchema(BaseModel):
    course_id: str = Field(alias="courseId")

    model_config = ConfigDict(populate_by_name=True)


class UpdateExerciseRequestSchema(ExerciseBase):
    pass


class UpdateExerciseResponseSchema(BaseModel):
    exercise: ExerciseSchema

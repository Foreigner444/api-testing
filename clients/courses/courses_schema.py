from typing import List

from pydantic import BaseModel, ConfigDict, Field

from clients.files.files_schema import FileSchema
from clients.users.users_schema import UserSchema
from tools.fakers import fake


class CourseSchema(BaseModel):
    id: str
    title: str
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    description: str
    preview_file: FileSchema = Field(alias="previewFile")
    estimated_time: str = Field(alias="estimatedTime")
    created_by_user_id: UserSchema = Field(alias="createdByUser")

    model_config = ConfigDict(populate_by_name=True)


class GetCoursesResponseSchema(BaseModel):
    courses: List[CourseSchema]


class CreateCourseResponseSchema(BaseModel):
    course: CourseSchema


class CreateCourseRequestSchema(BaseModel):
    title: str = Field(default_factory=fake.sentence)
    max_score: int = Field(alias="maxScore", default_factory=fake.max_score)
    min_score: int = Field(alias="minScore", default_factory=fake.min_score)
    description: str = Field(default_factory=fake.text)
    preview_file_id: str = Field(alias="previewFileId", default_factory=fake.uuid4)
    estimated_time: str = Field(
        alias="estimatedTime", default_factory=fake.estimated_time
    )
    created_by_user_id: str = Field(alias="createdByUserId", default_factory=fake.uuid4)

    model_config = ConfigDict(populate_by_name=True)


class UpdateCourseRequestSchema(BaseModel):
    title: str = Field(default_factory=fake.sentence)
    max_score: int = Field(alias="maxScore", default_factory=fake.max_score)
    min_score: int = Field(alias="minScore", default_factory=fake.min_score)
    description: str = Field(default_factory=fake.text)
    created_by_user_id: str = Field(alias="createdByUserId", default_factory=fake.uuid4)

    model_config = ConfigDict(populate_by_name=True)


class GetCoursesQuerySchema(BaseModel):
    user_id: str = Field(alias="userId")

    model_config = ConfigDict(populate_by_name=True)


class UpdateCourseResponseSchema(BaseModel):
    course: CourseSchema

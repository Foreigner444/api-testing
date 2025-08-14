from pydantic import BaseModel, Field, HttpUrl, FilePath
from tools.fakers import fake


class FileSchema(BaseModel):
    id: str
    filename: str
    directory: str
    url: HttpUrl


class CreateFileResponseSchema(BaseModel):
    file: FileSchema


class CreateFileRequestSchema(BaseModel):
    filename: str = Field(default_factory=lambda: f"{fake.uuid4()[:8]}.png")
    directory: str = Field(default="test")
    upload_file: FilePath


class GetFileResponseSchema(BaseModel):
    file: FileSchema

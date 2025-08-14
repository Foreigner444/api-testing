from pydantic import BaseModel, ConfigDict, EmailStr, Field

from tools.fakers import fake


class UserSchema(BaseModel):
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")

    model_config = ConfigDict(populate_by_name=True)


class CreateUserRequestSchema(BaseModel):
    email: EmailStr = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)
    last_name: str = Field(alias="lastName", default_factory=fake.last_name)
    first_name: str = Field(alias="firstName", default_factory=fake.first_name)
    middle_name: str = Field(alias="middleName", default_factory=fake.middle_name)

    model_config = ConfigDict(populate_by_name=True)


class GetUserResponseSchema(BaseModel):
    user: UserSchema


class CreateUserResponseSchema(BaseModel):
    user: UserSchema


class UpdateUserRequestSchema(BaseModel):
    first_name: str | None = Field(alias="firstName", default_factory=fake.first_name)
    last_name: str | None = Field(alias="lastName", default_factory=fake.last_name)
    middle_name: str | None = Field(
        alias="middleName", default_factory=fake.middle_name
    )
    email: EmailStr | None = Field(default_factory=fake.email)

    model_config = ConfigDict(populate_by_name=True)


class UpdateUserResponseSchema(BaseModel):
    user: UserSchema

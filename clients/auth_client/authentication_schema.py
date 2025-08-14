from pydantic import BaseModel, ConfigDict, EmailStr, Field

from tools.fakers import fake


class TokenSchema(BaseModel):
    token_type: str = Field(alias="tokenType")
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")

    model_config = ConfigDict(populate_by_name=True)


class LoginResponseSchema(BaseModel):
    token: TokenSchema


class LoginRequestSchema(BaseModel):
    email: EmailStr = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)


class RefreshRequestSchema(BaseModel):
    refresh_token: str = Field(alias="refreshToken", default_factory=fake.uuid4)

    model_config = ConfigDict(populate_by_name=True)

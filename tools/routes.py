from enum import Enum


class APIRoutes(str, Enum):
    AUTHENTICATION = "/api/v1/authentication"
    USERS = "/api/v1/users"
    FILES = "/api/v1/files"
    EXERCISES = "/api/v1/exercises"
    COURSES = "/api/v1/courses"

    def __str__(self):
        return self.value
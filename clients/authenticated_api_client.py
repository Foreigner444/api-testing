from clients.courses.courses_api_client import PrivateCoursesClient
from clients.exercises.exercises_api_client import PrivateExercisesClient
from clients.files.files_client import PrivateFilesClient
from clients.private_http_builder import (
    AuthenticationUserSchema,
    get_private_http_client,
)
from clients.users.private_users_client import PrivateUsersClient


class AuthenticatedApiClient:
    def __init__(self, user: AuthenticationUserSchema):
        self.client = get_private_http_client(user=user)
        self._users = None
        self._files = None
        self._courses = None
        self._exercises = None

    @property
    def users(self) -> PrivateUsersClient:
        if self._users is None:
            self._users = PrivateUsersClient(client=self.client)
        return self._users

    @property
    def files(self) -> PrivateFilesClient:
        if self._files is None:
            self._files = PrivateFilesClient(client=self.client)
        return self._files

    @property
    def courses(self) -> PrivateCoursesClient:
        if self._courses is None:
            self._courses = PrivateCoursesClient(client=self.client)
        return self._courses

    @property
    def exercises(self) -> PrivateExercisesClient:
        if self._exercises is None:
            self._exercises = PrivateExercisesClient(client=self.client)
        return self._exercises

from typing import Any

from httpx import URL, Client, QueryParams, Response
from httpx._types import RequestData, RequestFiles

from config import settings
import allure


class ApiClient:
    def __init__(self, client: Client | None = None):
        self.client = client if client else Client(base_url=settings.http_client.client_url)

    @allure.step("Make GET request to {url}")
    def get(self, url: URL | str, params: QueryParams | None = None) -> Response:
        response = self.client.get(url=url, params=params)
        return response

    @allure.step("Make POST request to {url}")
    def post(
        self,
        url: URL | str,
        json: Any | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
    ) -> Response:
        response = self.client.post(url=url, json=json, data=data, files=files)
        return response

    @allure.step("Make PATCH request to {url}")
    def patch(self, url: URL | str, json: Any | None = None) -> Response:
        response = self.client.patch(url=url, json=json)
        return response

    @allure.step("Make DELETE request to {url}")
    def delete(self, url: URL | str) -> Response:
        response = self.client.delete(url=url)
        return response

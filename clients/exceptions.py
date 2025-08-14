# from httpx import Response
#
#
# class ApiClientError(Exception):
#     def __init__(self, response: Response):
#         self.response = response
#         self.status_code = response.status_code
#         try:
#             self.details = response.json()
#         except Exception:
#             self.details = response.text
#         super().__init__(f"API request failed with status {self.status_code}: {self.details}")

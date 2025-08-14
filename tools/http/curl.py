import shlex
from typing import  Any
from httpx import Request, RequestNotRead, post


def make_curl_from_request(request: Request) -> str:
    """Converts an httpx.Request object into a curl command string,
    formatted across multiple lines for better readability."""

    # Start with the core 'curl' command, method, and URL.
    # These typically form the first logical line of the command.
    parts = [f"curl -X '{request.method}' '{request.url}'"]

    # Add headers, each on a new line
    for header, value in request.headers.items():
        # -H is the curl option for headers
        # shlex.quote ensures that header name/value with spaces or special characters are handled correctly
        parts.append(f"-H '{header}': '{value}'")

    # Add the request body, if present, on a new line
    try:
        body = request.content
        if body:
            # -d is the curl option for data (request body)
            # body.decode("utf-8") converts bytes content to a readable string
            parts.append(f"-d '{body.decode('utf-8')}'")
    except RequestNotRead:
        # If the body hasn't been read (e.g., streaming request not consumed yet),
        # we skip adding it to the curl command.
        pass
    return " \\\n  ".join(parts)

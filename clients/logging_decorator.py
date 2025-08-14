from functools import wraps

from clients.logger import get_logger

logger = get_logger(__name__)


def log_api_call(func):
    """
    A decorator that logs the class and method name of an API call and prints the response.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # The first argument is 'self' for instance methods
        class_name = args[0].__class__.__name__
        func_name = func.__name__

        logger.info(
            f"--- Calling {class_name}.{func_name} ---",
            extra={"func_args": args[1:], "func_kwargs": kwargs},
        )
        try:
            response = func(*args, **kwargs)
            logger.info(
                f"--- Response from {class_name}.{func_name} ---",
                extra={"response": response},
            )
            return response
        except Exception as e:
            logger.error(
                f"--- Error in {class_name}.{func_name} ---",
                extra={"exception_type": type(e).__name__, "exception_message": str(e)},
            )
            raise

    return wrapper

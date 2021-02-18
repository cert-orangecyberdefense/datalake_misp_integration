from typing import Type

from src.logger import logger


def ignore(exception: Type[Exception], message: str):
    """Ignore exception when raised in the function and instead log the message passed"""
    def inner_decorator(function):
        def wrapper(*args, **kwargs):
            response = None
            try:
                response = function(*args, **kwargs)
            except exception:
                logger.exception(message)
            return response
        return wrapper
    return inner_decorator

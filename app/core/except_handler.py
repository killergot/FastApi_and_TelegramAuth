from functools import wraps
from typing import Callable
import logging

log = logging.getLogger(__name__)

def except_handler(method : Callable) -> Callable:
    '''Простой декоратор для отлавливания ошибок'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            result = method(self, *args, **kwargs)
            return result
        except:
            log.exception(f"Error in {method.__name__}")
            return None
    return wrapper
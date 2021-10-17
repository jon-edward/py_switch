from __future__ import annotations
from typing import Type, Any, TypeVar


class _InvalidCase:
    """Sentinel object for defining when a case is not met."""
    pass


_INVALID_CASE = _InvalidCase()

_CASE_FLAG_NAME = "_is_case_method"


#  A case is 'default' when its predicate is always true.
#  Declaring a variable named 'default' is simply to increase
#  readability for the user.
default = True


def resolve(s: Type[switch]) -> Any:
    """Decorator for auto-resolving switch statement when it is referenced, and returning the result."""
    return s.eval()


class switch:
    """
    Is a switch-case implementation.

    Note: If a default value is defined before other values, it will always return before them no matter if they are
    actually accepted or not.
    """
    __slots__ = []

    value: Any

    @staticmethod
    def case(predicate):
        """A decorator that defines default behavior for case function definitions in a class."""
        is_correct_case = bool(predicate)

        def decorator(function):
            def wrapper(*args, **kwargs):
                if not is_correct_case:
                    return _INVALID_CASE
                result = function(*args, **kwargs)
                return result
            wrapper.__setattr__(_CASE_FLAG_NAME, True)
            return wrapper
        return decorator

    @classmethod
    def eval(cls):
        """Resolves the switch statement, and returns the accepted case's returning value."""
        case_methods = [
            x for x in cls.__dict__.values() if callable(x) and x.__dict__.get(_CASE_FLAG_NAME, False)
        ]
        for func in case_methods:
            result = func(cls)
            if result is not _INVALID_CASE:
                return result
        return None

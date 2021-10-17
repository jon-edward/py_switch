from __future__ import annotations
from typing import Type, Any


class _InvalidCase:
    """Sentinel object for defining when a case is not met."""


_INVALID_CASE = _InvalidCase()


class _UndefinedEval:
    """Sentinel object for defining when a switch statement has not been evaluated yet."""


_UNDEFINED_EVAL = _UndefinedEval()


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

    Use by inheriting from this class, decorating case methods with
    `case(predicate)`, and optionally decorating subclass with `resolve`
    to evaluate the switch-case statement on first reference.
    """

    __slots__ = []

    _cached_eval = _UNDEFINED_EVAL

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
        if cls._cached_eval is not _UNDEFINED_EVAL:
            return cls._cached_eval

        case_methods = [
            x
            for x in cls.__dict__.values()
            if callable(x) and x.__dict__.get(_CASE_FLAG_NAME, False)
        ]
        for func in case_methods:
            result = func(cls)
            if result is not _INVALID_CASE:
                cls._cached_eval = result
                return result
        return None

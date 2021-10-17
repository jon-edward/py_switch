from __future__ import annotations


class _InvalidCase:
    """Sentinel object for defining when a case is not met."""
    pass


_INVALID_CASE = _InvalidCase()


#  A case is 'default' when its predicate is always true.
#  Declaring a variable named 'default' is simply to increase
#  readability for the user.
default = True


class switch:
    """
    Is a switch-case implementation.

    Note: If a default value is defined before other values, it will always return before them no matter if they are
    actually accepted or not.
    """
    __slots__ = []

    def __call__(self, f: switch):
        """This is called when `switch` is used as a decorator."""
        return switch.eval(f)

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
            return wrapper
        return decorator

    def eval(self):
        """Resolves the switch statement, and returns the accepted case's returning value."""
        functions = [
            getattr(self, x) for x in self.__dict__ if
            not x.startswith("__") and x != "value"
        ]
        for func in functions:
            result = func(self)
            if result is not _INVALID_CASE:
                return result

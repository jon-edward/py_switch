from __future__ import annotations


class _InvalidCase:
    pass


_INVALID_CASE = _InvalidCase()


default = True


class switch:
    __slots__ = []

    def __call__(self, f: switch):
        return switch.eval(f)

    @staticmethod
    def case(predicate):
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
        functions = [
            getattr(self, x) for x in self.__dict__ if
            not x.startswith("__") and x != "value"
        ]
        for func in functions:
            result = func(self)
            if result is not _INVALID_CASE:
                return result

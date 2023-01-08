"""Define a non-negative counter object."""
from collections import Counter


class NegativeNumberError(ValueError):
    def __init__(self, message="values must be non-negative"):
        super().__init__(message)


class SubtractionError(ValueError):
    def __init__(self, message="subtraction would drop count below zero"):
        super().__init__(message)


class NNCounter(Counter):
    def __init__(self, iterable=None, /, **kwds):
        """
        Create a new NNCounter object.
        """
        if (
            iterable is not None
            and issubclass(type(iterable), dict)
            and any([x < 0 for x in iterable.values()])
        ):
            raise NegativeNumberError

        if kwds and any([x < 0 for x in kwds.values()]):
            raise NegativeNumberError
        super().__init__()
        self.update(iterable, **kwds)

    # def __add__(self, other):
    #     """
    #     Add counts from two counters.
    #     """
    #     if not isinstance(other, NNCounter):
    #         return NotImplemented
    #     result = NNCounter()
    #     for elem, count in self.items():
    #         newcount = count + other[elem]
    #         if newcount > 0:
    #             result[elem] = newcount
    #         if newcount < 0:
    #             raise NegativeNumberError
    #     for elem, count in other.items():
    #         if elem not in self and count > 0:
    #             result[elem] = count
    #     return result
    def __isub__(self, other):
        """
        Inplace subtract counter.

        Raises a SubtractionError if any count drops below 0.
        """
        for elem, count in other.items():
            newcount = self[elem] - count
            if newcount < 0:
                raise SubtractionError
            else:
                self[elem] = newcount
        return self

    def __setitem__(self, k, v):
        if v < 0:
            raise NegativeNumberError
        else:
            super().__setitem__(k, v)

    def __sub__(self, other):
        """
        Subtract one NNCounter from another.

        Raises a SubtractionError if any count drops below 0.
        """
        if not isinstance(other, NNCounter):
            return NotImplemented
        result = NNCounter()
        for elem, count in self.items():
            newcount = count - other[elem]
            if newcount > 0:
                result[elem] = newcount
            elif newcount < 0:
                raise SubtractionError
        for elem, count in other.items():
            if elem not in self and count > 0:
                raise SubtractionError

        return result

    def subtract(self, *args, **kwargs):
        other = NNCounter(*args, **kwargs)
        self -= other


# TODO: subtract

from inspect import isclass, ismodule

from .strings import cut_prefix


__all__ = ['cached_property', 'monkey']


class cached_property(object):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    NOTE: implementation borrowed from Django.
    NOTE: we use fget, fset and fdel attributes to mimic @property.
    """
    fset = fdel = None

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        res = instance.__dict__[self.fget.__name__] = self.fget(instance)
        return res


def monkey(cls):
    assert isclass(cls) or ismodule(cls), "Attempting to monkey patch non-class and non-module"

    def decorator(value):
        func = getattr(value, 'fget', value) # Support properties
        name = cut_prefix(func.__name__, '%s__' % cls.__name__)

        func.__name__ = name
        func.original = getattr(cls, name, None)

        setattr(cls, name, value)
        return value
    return decorator


# TODO: monkey_mix()?

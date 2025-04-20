from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(x.value, x.name) for x in cls]

    @classmethod
    def names(cls):
        return list(x.name for x in cls)

    @classmethod
    def values(cls):
        return list(x.value for x in cls)

    @classmethod
    def max_length(cls):
        return max(len(x.value) for x in cls)

    @classmethod
    def count(cls):
        return len(cls)

    @classmethod
    def mapping(cls):
        return dict((x.name, x.value) for x in cls)

class BasePermissions:
    @classmethod
    def mapping(cls):
        return {name: value for name, value in cls.__dict__.items() if not name.startswith('__') and not callable(value)}
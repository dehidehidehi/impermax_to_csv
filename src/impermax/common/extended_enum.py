from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        """Lists all the values of this Enum."""
        return list(map(lambda c: c.value, cls))

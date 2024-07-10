from enum import Enum, EnumMeta


class ContainsMeta(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True


class BaseEnum(str, Enum, metaclass=ContainsMeta):
    """Base enum subclass, that allows to check if value is in enum"""

    # noinspection PyMethodParameters,PyTypeChecker
    def _generate_next_value_(name, start, count, last_values) -> str:  # type: ignore
        """
        Uses the name as the automatic value, rather than an integer
        See https://docs.python.org/3/library/enum.html#using-automatic-values for reference
        """
        return name



class TarifType(BaseEnum):
    FREE = 'free'
    PRIVATE = 'private'
    PRO = 'pro'


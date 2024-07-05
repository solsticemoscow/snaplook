from enum import Enum, EnumMeta

from app.config import settings


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


class DB_TYPE(BaseEnum):
    db_async: str = settings.POSTGRES_URL_ASYNC
    db_sync: str = settings.POSTGRES_URL_SYNC


class TestInference(BaseEnum):
    uuid_90 = '55bb13ed-fb5d-4f31-999e-beacb8383726'
    uuid_30 = '330d8a4c-e5b9-422c-a69c-6e643825feb4'


class Role(BaseEnum):
    """User Roles"""
    USER = 0
    ADMIN = 1
    SUPERADMIN = 2


class SeriesStatus(BaseEnum):
    """Stages of Scan processing"""
    RECEIVED = 'received'
    IN_PROGRESS = 'in-progress'
    FINISHED = 'finished'
    ERROR = 'error'

class Status(BaseEnum):
    """Stages of Scan processing"""
    RECEIVED = 'received'
    IN_PROGRESS = 'in-progress'
    FINISHED = 'finished'
    ERROR = 'error'

class TypeofInference(BaseEnum):
    ONE = 'one'
    SERIES = 'series'
    PACS = 'pacs'

class InferenceStatus(BaseEnum):
    """Stages of Scan processing"""
    RECEIVED = 'received'
    IN_PROGRESS = 'in-progress'
    FINISHED = 'finished'
    ERROR = 'error'


class InferenceType(BaseEnum):
    """Stages of Scan processing"""
    T2 = 't2'
    DWI = 'dwi'
    ADC = 'adc'
    DCE = 'dce'
    NONE = None


class Diagnostic(BaseEnum):
    RADIOLOGY = 'radiology'
    PATHOLOGY = 'pathology'
    ENDOSCOPY = 'endoscopy'


class Organ(BaseEnum):
    PROSTATE = 'prostate'
    COLON = 'colon'
    BLADDER = 'bladder'


class JobType(BaseEnum):
    INFERS = 'infers'
    ACTIVE_LEARNING = 'active-learning'


class Method(BaseEnum):

    SEGMENTATION = 'segmentation'
    CLASSIFICATION = 'classification'
    SIMILAR_CASES = 'similar-cases'


class ProcessingStage(BaseEnum):
    RECEIVED = 'received'
    IN_PROGRESS = 'in-progress'
    FINISHED = 'finished'
    ERROR = 'error'


# class Status(BaseEnum):
#     """Stages of Scan processing"""
#     NOT_SENT = 'not-sent'
#     IN_PROGRESS = 'in-progress'
#     FINISHED = 'finished'
#     ERROR = 'error'


class Stage(BaseEnum):
    """Stages of Scan processing"""
    NOT_SENT = 'not-sent'
    IN_PROGRESS = 'in-progress'
    FINISHED = 'finished'
    ERROR = 'error'

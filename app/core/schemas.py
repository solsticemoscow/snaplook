from typing import Optional, List
from datetime import datetime
import uuid

from pydantic import BaseModel


from app.models import enums as en


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        underscore_attrs_are_private = True
        use_enum_values = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenSchema(BaseSchema):
    access_token: str
    refresh_token: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: float




class UserModelCreate(BaseSchema):
    login: str
    password: str
    role: en.Role = en.Role.USER
    is_active: bool = True




class UserModelRead(BaseSchema):
    id: int = None
    login: str
    role: en.Role = en.Role.USER
    is_active: bool = True
    created_at: datetime


class UserModelChange(BaseSchema):
    id: int = None
    login: str
    password: str
    role: en.Role = en.Role.USER
    is_active: bool = True


class InferencePost(BaseSchema):
    id: uuid.UUID
    diagnostic: en.Diagnostic = en.Diagnostic.RADIOLOGY
    method: en.Method = en.Method.CLASSIFICATION
    job_type: en.JobType = en.JobType.INFERS
    organ: en.Organ = en.Organ.PROSTATE


class PresignedPost(BaseModel):
    url: str = ''
    fields: dict = {}


class InferenceResponse(BaseSchema):
    id: uuid.UUID
    clinic_id: Optional[uuid.UUID]

    created_at: datetime
    proceed_at: Optional[datetime]
    status: en.InferenceStatus
    images_number: Optional[int]

    diagnostic: en.Diagnostic = en.Diagnostic.RADIOLOGY
    method: en.Method = en.Method.CLASSIFICATION
    job_type: en.JobType = en.JobType.INFERS
    organ: en.Organ = en.Organ.PROSTATE

    presigned_post: Optional[PresignedPost]


class MLResult(BaseSchema):
    filename: str
    probability_slice: Optional[str]
    mask1: Optional[str] = None
    mask2: Optional[str]
    mask3: Optional[str]
    error: Optional[str]


class InferenceResult(BaseSchema):
    id: uuid.UUID
    status: en.InferenceStatus
    error: Optional[str]

    data: List[MLResult]


class InferenceFinishResp(BaseSchema):
    status: str
    result: str

class InferenceSeg(BaseSchema):
    mask2: str
    mask3: str

class ClinicResponse(BaseSchema):
    id: uuid.UUID
    name: str
    is_active: bool
    created_at: datetime
    s3_bucket: str

class TestInfResponse(BaseSchema):
    status: str
    filename: str
    speed: float

class ClinicPost(BaseSchema):
    name: str
    is_active: bool = True
    s3_bucket: Optional[str]

class TestResponse(BaseSchema):
    test: Optional[str]

class TestPost(BaseSchema):
    test: Optional[str]

class InferenceTestPost(BaseSchema):
    test_uuid: en.TestInference



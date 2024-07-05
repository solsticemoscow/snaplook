

from pydantic import BaseModel



# class BaseSchema(BaseModel):
#     class Config:
#         orm_mode = True
#         underscore_attrs_are_private = True
#         use_enum_values = True



class Token(BaseModel):
    access_token: str
    token_type: str

# class Token(BaseSchema):
#
#     """Validated access token with type."""
#
#     access_token: str
#     expires_in: int
#     refresh_expires_in: int
#     refresh_token: str
#     token_type: str = "Bearer"
#     id_token: str
#     beforepolicy: int = Field(default="not-before-policy")
#     session_state: str
#     scope: str
#
# class User(BaseModel):
#     username: str
#     id: str
#     email: str | None = None
#     first_name: str | None
#     last_name: str | None
#     client_roles: list | None = None
#     realm_roles: list | None = None
#
#
# ######################## Inference ########################
#
# class TaskSchema(BaseSchema):
#     id: str = str(uuid.uuid4())
#
#     username: str
#     type: TypeofInference
#
#     cln_id: str = settings.CLINIC_ID
#     dev_id: str = settings.DEVICE_UID
#
#     images_number: int = 0
#     created_at: datetime = datetime.now()
#
#     status: Status
#     diagnostic: en.Diagnostic = Diagnostic.RADIOLOGY
#     method: en.Method = Method.CLASSIFICATION
#     organ: en.Organ = Organ.PROSTATE
#
#
# class InferenceItem(TypedDict):
#     filename: str
#     probability_slice: str
#
# class InferenceCheck(TypedDict):
#     id: str
#     url: Url
#     data: List[InferenceItem]
#
# ######################## Series ########################
#
#
#
# class SeriesItem(TypedDict):
#     filename: str
#     probability_slice: str
#
# class SeriesCheck(TypedDict):
#     id: str
#     url: Url
#     data: List[SeriesItem]
#
# ######################## Other ########################
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

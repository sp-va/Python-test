from pydantic import BaseModel, Field, field_validator
import datetime as dt
from typing import List

from src.users.schemas import UserModelSchema

class PicnicInSchema(BaseModel):
    city_id: int
    time: dt.datetime = Field(..., example="2023-09-11 20:00:00")
    
    @field_validator('time')
    def time_not_past(cls, time):
        if time.timestamp() < dt.datetime.now().timestamp():
            raise ValueError('You cannot create picnic in past')
        return time
    
class SinglePicnicOutSchema(BaseModel):
    id: int
    city: str
    time: dt.datetime = Field

    class Config:
        from_attributes = True

class ManyPicnicsOutSchema(SinglePicnicOutSchema,):
    users: List[UserModelSchema] = [] 
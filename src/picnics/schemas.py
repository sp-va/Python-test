from pydantic import BaseModel, validator
import datetime as dt

from src.users.schemas import UserModelSchema

class PicnicInSchema(BaseModel):
    city_id: int
    time: dt.datetime
    
    @validator('time')
    def time_not_past(cls, time):
        if time.timestamp() < dt.datetime.now().timestamp():
            raise ValueError('You cannot create picnic in past')
        return time
    
class SinglePicnicOutSchema(BaseModel):
    id: int
    city: str
    time: dt.datetime

    class Config:
        orm_mode = True
        from_attributes = True
class ManyPicnicsOutSchema(SinglePicnicOutSchema,):
    users: list[UserModelSchema]
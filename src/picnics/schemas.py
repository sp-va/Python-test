from pydantic import BaseModel, validator
import datetime as dt

class PicnicInSchema(BaseModel):
    city_id: int
    time: dt.datetime
    
    @validator('time')
    def time_not_past(cls, time):
        if time.timestamp() < dt.datetime.now().timestamp():
            raise ValueError('You cannot create picnic in past')
        return time
    
class PicnicOutSchema(BaseModel):
    id: int
    city: str
    time: dt.datetime

    class Config:
        orm_mode = True
        from_attributes = True
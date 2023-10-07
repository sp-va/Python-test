from pydantic import BaseModel, validator
import datetime as dt

class CityOutSchema(BaseModel):
    id: int
    name: str
    weather: float

    class Config:
        orm_mode = True

class RegisterUserRequestSchema(BaseModel):
    name: str
    surname: str
    age: int

    @validator('age')
    def age_valid(cls, age):
        if age < 0 or age > 150:
            raise ValueError("Age must be greater than 0 and less than 150!")
        return age
    
class UserModelSchema(RegisterUserRequestSchema):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

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

class PicnicRegistrationSchema(BaseModel):
    user_id: int
    picnic_id: int

    class Config:
        from_attributes = True
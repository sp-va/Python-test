from pydantic import BaseModel

class CityOutSchema(BaseModel):
    id: int
    name: str
    weather: float

    class Config:
        orm_mode = True

class RegisterUserRequest(BaseModel):
    name: str
    surname: str
    age: int


class UserModel(BaseModel):
    id: int
    name: str
    surname: str
    age: int

    class Config:
        orm_mode = True



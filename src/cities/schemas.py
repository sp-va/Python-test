from pydantic import BaseModel, validator

class CityOutSchema(BaseModel):
    id: int
    name: str
    weather: float

    class Config:
        orm_mode = True


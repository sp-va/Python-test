from pydantic import BaseModel, validator

class CityOutSchema(BaseModel):
    id: int
    name: str
    weather: float

    class Config:
        from_attributes = True

class CityAddSchema(BaseModel):
    name: str

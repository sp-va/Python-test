from pydantic import BaseModel, field_validator

class RegisterUserRequestSchema(BaseModel):
    name: str
    surname: str
    age: int

    @field_validator('age')
    def age_valid(cls, age):
        if age < 0 or age > 150:
            raise ValueError("Age must be greater than 0 and less than 150!")
        return age
    
class UserModelSchema(RegisterUserRequestSchema):
    id: int

    class Config:
        from_attributes = True
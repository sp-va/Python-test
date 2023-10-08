from pydantic import BaseModel

class PicnicRegistrationSchema(BaseModel):
    user_id: int
    picnic_id: int

    class Config:
        from_attributes = True
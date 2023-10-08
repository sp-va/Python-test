from fastapi import APIRouter, HTTPException, Depends

from src.database import Session, get_session
from src.users.models import *
from src.picnics.models import *
from src.registration.models import *
from src.registration.schemas import *

router = APIRouter(
    prefix='/registration',
    tags=['registration'],
)

@router.post('/add/', summary='Picnic Registration', response_model=PicnicRegistrationSchema)
def register_to_picnic(registration_data: PicnicRegistrationSchema, session: Session = Depends(get_session)):
    """
    Регистрация пользователя на пикник
    (Этот эндпойнт необходимо реализовать в процессе выполнения тестового задания)
    """
    user = session.query(User).get(registration_data.user_id)
    picnic = session.query(Picnic).get(registration_data.picnic_id)
    registration_object = PicnicRegistration(**registration_data.dict())

    if not user or not picnic:
        raise HTTPException(status_code=400, detail='User and Picnic must be in DB')

    session.add(registration_object)
    session.commit()

    return PicnicRegistrationSchema.from_orm(registration_object)

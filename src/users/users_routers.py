from fastapi import APIRouter, HTTPException, Depends

from src.users.models import *
from src.users.schemas import *
from src.database import get_session, Session

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

@router.get('/get/', summary='Get users list', response_model=list[UserModelSchema])
def users_list(min_age: int = 0, max_age: int = 200, session: Session = Depends(get_session)):
    """
    Список пользователей
    """
    if min_age < max_age:
        users = session.query(User).filter(min_age < User.age, User.age < max_age).all()
        return users
    else:
        raise HTTPException(status_code=404, detail='Minimal age must be less than maximum age!')


@router.post('/add/', summary='CreateUser', response_model=UserModelSchema)
def register_user(user: RegisterUserRequestSchema, session: Session = Depends(get_session)):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    session.add(user_object)
    session.commit()
    return UserModelSchema.from_orm(user_object)
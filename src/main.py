import datetime as dt
from fastapi import FastAPI, HTTPException, Query, Depends
from typing import Union

from src.models import City, User, Picnic, PicnicRegistration
from src.database import Session, get_session
from src.external_requests import CheckCityExisting, GetWeatherRequest
from src.schemas import *

app = FastAPI()


@app.post('/create-city/', summary='Create City', description='Создание города по его названию')
def create_city(city: str = Query(description="Название города", default=None), session: Session = Depends(get_session)):
    if city is None:
        raise HTTPException(status_code=400, detail='Параметр city должен быть указан')
    check = CheckCityExisting()
    if not check.check_existing(city):
        raise HTTPException(status_code=400, detail='Параметр city должен быть существующим городом')

    city_object = session.query(City).filter(City.name == city.capitalize()).first()
    if city_object is None:
        city_object = City(name=city.capitalize())
        session.add(city_object)
        session.commit()

    return {'id': city_object.id, 'name': city_object.name, 'weather': city_object.weather}


@app.get('/get-cities/', summary='Get Cities', response_model=Union[CityOutSchema, list[CityOutSchema]])
def cities_list(q: str = Query(description="Название города", default=None), session: Session = Depends(get_session)):
    """
    Получение списка городов
    """
    if q:
        city = session.query(City).filter(City.name==q).first()
        if city:
            return {'id': city.id, 'name': city.name, 'weather': city.weather}
        else:
            raise HTTPException(status_code=404, detail='The city is not in DB')
    else:
        cities = session.query(City).all()
        return cities


@app.get('/users-list/', summary='Get users list', response_model=list[UserModelSchema])
def users_list(min_age: int = 0, max_age: int = 200, session: Session = Depends(get_session)):
    """
    Список пользователей
    """
    if min_age < max_age:
        users = session.query(User).filter(min_age < User.age, User.age < max_age).all()
        return users
    else:
        raise HTTPException(status_code=404, detail='Minimal age must be less than maximum age!')


@app.post('/register-user/', summary='CreateUser', response_model=UserModelSchema)
def register_user(user: RegisterUserRequestSchema, session: Session = Depends(get_session)):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    session.add(user_object)
    session.commit()
    return UserModelSchema.from_orm(user_object)


@app.get('/all-picnics/', summary='All Picnics', tags=['picnic'])
def all_picnics(datetime: dt.datetime = Query(default=None, description='Время пикника (по умолчанию не задано)'),
                past: bool = Query(default=True, description='Включая уже прошедшие пикники')):
    """
    Список всех пикников
    """
    picnics = Session().query(Picnic)
    if datetime is not None:
        picnics = picnics.filter(Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())

    return [{
        'id': pic.id,
        'city': Session().query(City).filter(City.id == pic.id).first().name,
        'time': pic.time,
        'users': [
            {
                'id': pr.user.id,
                'name': pr.user.name,
                'surname': pr.user.surname,
                'age': pr.user.age,
            }
            for pr in Session().query(PicnicRegistration).filter(PicnicRegistration.picnic_id == pic.id)],
    } for pic in picnics]


@app.post('/picnic-add/', summary='Picnic Add', tags=['picnic'], response_model=PicnicOutSchema)
def picnic_add(picnic: PicnicInSchema, session: Session = Depends(get_session)):
    picnic_object = Picnic(**picnic.dict())
    city = session.query(City).get(picnic.city_id)

    if not city:
        raise HTTPException(status_code=400, detail=f'City with id {picnic.city_id} is not in DB')
    
    session.add(picnic_object)
    session.commit()

    return {
        'id': picnic_object.id,
        'city': city.name,
        'time': picnic_object.time,
    }


@app.post('/picnic-register/', summary='Picnic Registration', tags=['picnic'], response_model=PicnicRegistrationSchema)
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

    

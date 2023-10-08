from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Union

from src.cities.models import City
from src.cities.schemas import *
from src.utils.external_requests import CheckCityExisting
from src.database import Session, get_session

router = APIRouter(
    prefix='/cities',
    tags=['cities'],
)

@router.post('/add/', summary='Add new city', description='Создание города по его названию', response_model=CityOutSchema)
def create_city(city: CityAddSchema, session: Session = Depends(get_session)):
    if city.name is None:
        raise HTTPException(status_code=400, detail='Параметр city должен быть указан')
    
    check = CheckCityExisting()

    if not check.check_existing(city.name):
        raise HTTPException(status_code=400, detail='Параметр city должен быть существующим городом')

    city_object = session.query(City).filter(City.name == city.name.capitalize()).first()
    if city_object is None:
        city_object = City(name=city.name.capitalize())
        session.add(city_object)
        session.commit()

    return city_object

@router.get('/get/', summary='Get Cities', response_model=Union[CityOutSchema, list[CityOutSchema]])
def cities_list(q: str = Query(description="Название города", default=None), session: Session = Depends(get_session)):
    """
    Получение списка городов
    """
    if q:
        city = session.query(City).filter(City.name==q).first()
        if city:
            return city
        else:
            raise HTTPException(status_code=404, detail='The city is not in DB')
    else:
        cities = session.query(City).all()
        return cities
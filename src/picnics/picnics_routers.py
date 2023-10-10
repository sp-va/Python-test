from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import joinedload
from sqlalchemy import union_all

from src.picnics.schemas import *
from src.picnics.models import *
from src.cities.models import *
from src.users.models import *
from src.registration.models import *
from src.database import Session, get_session

router = APIRouter(
    prefix='/picnics',
    tags=['picnics'],
)

@router.post('/add/', summary='Picnic Add', response_model=SinglePicnicOutSchema)
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

@router.get('/get/', summary='All Picnics', response_model=List[ManyPicnicsOutSchema])
def all_picnics(picnic_datetime: dt.datetime = Query(default=None, description='Время пикника (по умолчанию не задано)'),
                past: bool = Query(default=True, description='Включая уже прошедшие пикники'), session: Session = Depends(get_session)):
    """
    Список всех пикников
    """
    picnics = session.query(Picnic).options(joinedload(Picnic.city), joinedload(Picnic.users))
    filter_1 = False
    filter_2 = False

    if past:
        filter_1 = Picnic.time <= dt.datetime.now()
    if picnic_datetime:
        filter_2 = Picnic.time == picnic_datetime

    query_1 = picnics.filter(filter_1)
    query_2 = picnics.filter(filter_2)
    picnics = query_1.union_all(query_2)
    picnics = picnics.all()

    return [{
        'id': obj.id,
        'city': obj.city.name,
        'time': obj.time,
        'users': [
            {
                'name': u.user.name,
                'surname': u.user.surname,
                'age': u.user.age,
                'id': u.user.id,
            } for u in obj.users
        ]
    } for obj in picnics]
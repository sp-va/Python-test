from fastapi import APIRouter, HTTPException, Query, Depends

from src.picnics.schemas import *
from src.picnics.models import *
from src.cities.models import *
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

@router.get('/get/', summary='All Picnics', response_model=ManyPicnicsOutSchema)
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
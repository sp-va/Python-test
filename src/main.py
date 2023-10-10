from fastapi import FastAPI

from src.cities import cities_routers
from src.picnics import picnics_routers
from src.registration import registration_routers
from src.users import users_routers
from src.logger import app_logger

app = FastAPI()

@app.get('/')
def root():
    app_logger.info('info message')
    return {'response': 'good response'}

app.include_router(cities_routers.router)
app.include_router(picnics_routers.router)
app.include_router(registration_routers.router)
app.include_router(users_routers.router)









    

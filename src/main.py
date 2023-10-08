from fastapi import FastAPI

from src.cities import cities_routers
from src.picnics import picnics_routers
from src.registration import registration_routers
from src.users import users_routers

app = FastAPI()

app.include_router(cities_routers.router)
app.include_router(picnics_routers.router)
app.include_router(registration_routers.router)
app.include_router(users_routers.router)









    

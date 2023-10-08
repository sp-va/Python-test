from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.database import Base, engine

class Picnic(Base):
    """
    Пикник
    """
    __tablename__ = 'picnic'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    time = Column(DateTime, nullable=False)

    city = relationship('City', backref='picnics')

    def __repr__(self):
        return f'<Пикник {self.id}>'
    
Base.metadata.create_all(bind=engine)
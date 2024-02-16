from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date

from db import Base, engine

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    surname = Column(String(50))
    phone_number = Column(String(15))
    email = Column(String(40))
    birthday = Column(Date)
    notes = Column(String(200))

Base.metadata.create_all(bind=engine)
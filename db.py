from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:567234@localhost:5432/postgres"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# class Contact(Base):
#     __tablename__ = "contacts"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50))
#     surname = Column(String(50))
#     phone_number = Column(String(15))
#     birthday = Column(Date)
#     notes = Column(String(200))


# Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

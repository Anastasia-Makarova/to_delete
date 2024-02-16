from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session


from db import get_db
from models import Contact
from schemas import ContactSchema, ContactResponse


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello from HW 11"}


@app.get('/contacts', response_model=list[ContactResponse])
async def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    return contacts


@app.post('/contacts', response_model=ContactResponse)
async def create_contact(body: ContactSchema, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(email=body.email).first()
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Contact with this email already exists')
    contact = Contact(
        name=body.name, 
        surname=body.surname, 
        phone_number=body.phone_number, 
        email=body.email,
        birthday=body.birthday,
        notes=body.notes
        )
    db.add(contact)
    db.commit()
    # db.refresh()
    return contact



@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()  # noqa
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    # return {'message': 'Welcome!'}

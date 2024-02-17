from fastapi import FastAPI, Depends, HTTPException, status, Path
from sqlalchemy import text
from sqlalchemy.orm import Session



from db import get_db
from models import Contact
from schemas import ContactSchema, ContactResponse


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello from HW 11"}


@app.get("/contacts", response_model=list[ContactResponse])
async def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    return contacts


@app.get("/contacts/{contact_id}", response_model=ContactResponse, tags=["search_by_parameter"])
async def get_contact_by_id(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@app.get("/name", response_model=list[ContactResponse], tags=["search_by_parameter"])
async def get_contact_by_name(contact_name: str, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(name=contact_name).all()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@app.get("/surmane", response_model=list[ContactResponse], tags=["search_by_parameter"])
async def get_contact_by_surname(contact_surname: str, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(surname=contact_surname).all()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@app.get("/email", response_model=ContactResponse, tags=["search_by_parameter"])
async def get_contact_by_email(contact_email: str, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(email=contact_email).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


# @app.get("/birthdays", response_model=list[ContactResponse], tags=["search_by_parameter"])
# async def get_contact_by_email(start_date: str, db: Session = Depends(get_db)):
#     contact = db.query(Contact).filter_by(email=contact_email).first()
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
#     return contact


@app.post("/contacts", response_model=ContactResponse)
async def create_contact(body: ContactSchema, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(email=body.email).first()
    if contact:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Contact with this email already exists",
        )
    contact = Contact(
        name=body.name,
        surname=body.surname,
        phone_number=body.phone_number,
        email=body.email,
        birthday=body.birthday,
        notes=body.notes,
    )
    db.add(contact)
    db.commit()
    return contact


@app.put("/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    contact.name = (body.name,)
    contact.surname = (body.surname,)
    contact.phone_number = (body.phone_number,)
    contact.email = (body.email,)
    contact.birthday = (body.birthday,)
    contact.notes = body.notes

    db.commit()
    return contact


@app.delete("/contacts/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    db.delete(contact)
    db.commit()
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

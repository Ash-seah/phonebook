import fastapi
import generate_random_data
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+mysqlconnector://root:admin@localhost/phonebook").connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class NameNum(Base):
    __tablename__ = "name_num"
    name = Column(String, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    email = Column(String, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    session = SessionLocal()
    try:
        res = session.execute(select(NameNum).order_by(NameNum.name)).scalars().all()
        return [row.__dict__ for row in res]
    finally:
        session.close()

@app.put("/")
async def add_record(name: str, number: str, email: str):
    session = SessionLocal()
    try:
        new_record = NameNum(name=name, phone_number=number, email=email)
        session.add(new_record)
        session.commit()
        return {"message": "Record added successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@app.get("/query/name/")
async def query_name(name: str):
    session = SessionLocal()
    try:
        res = session.query(NameNum).filter(NameNum.name.ilike(f"%{name}%")).order_by(NameNum.name).all()
        return [row.__dict__ for row in res]
    finally:
        session.close()

@app.get("/query/number/")
async def query_number(number: str):
    session = SessionLocal()
    try:
        res = session.query(NameNum).filter(NameNum.phone_number.like(f"%{number}%")).order_by(NameNum.name).all()
        return [row.__dict__ for row in res]
    finally:
        session.close()

@app.get("/query/email/")
async def query_email(email: str):
    session = SessionLocal()
    try:
        res = session.query(NameNum).filter(NameNum.email.like(f"%{email}%")).order_by(NameNum.name).all()
        return [row.__dict__ for row in res]
    finally:
        session.close()

@app.delete("/delete/")
async def delete_record(name: str):
    session = SessionLocal()
    try:
        record_to_delete = session.query(NameNum).filter(NameNum.name == name).first()
        if record_to_delete:
            session.delete(record_to_delete)
            session.commit()
            return {"message": "Record deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Record not found")
    finally:
        session.close()

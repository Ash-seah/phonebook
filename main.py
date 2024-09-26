from fastapi import FastAPI, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+mysqlconnector://root:admin@localhost/phonebook").connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

REQUESTS_PER_MINUTE = 20

class NameNum(Base):
    __tablename__ = "name_num"
    name = Column(String, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    email = Column(String, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Initialize the limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

@app.get("/")
@limiter.limit(f"{REQUESTS_PER_MINUTE}/minute")
async def root(request: Request):
    session = SessionLocal()
    try:
        res = session.execute(select(NameNum).order_by(NameNum.name)).scalars().all()
        return [row.__dict__ for row in res]
    finally:
        session.close()

@app.put("/")
@limiter.limit(f"{REQUESTS_PER_MINUTE}/minute")
async def add_record(request: Request, name: str, number: str, email: str):
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
@limiter.limit(f"{REQUESTS_PER_MINUTE}/minute")
async def query_name(request: Request, name: str):
    session = SessionLocal()
    try:
        res = session.query(NameNum).filter(NameNum.name.ilike(f"%{name}%")).order_by(NameNum.name).all()
        return [row.__dict__ for row in res]
    finally:
        session.close()

@app.get("/query/number/")
@limiter.limit(f"{REQUESTS_PER_MINUTE}/minute")
async def query_number(request: Request, number: str):
    session = SessionLocal()
    try:
        res = session.query(NameNum).filter(NameNum.phone_number.like(f"%{number}%")).order_by(NameNum.name).all()
        return [row.__dict__ for row in res]
    finally:
        session.close()

@app.get("/query/email/")
@limiter.limit(f"{REQUESTS_PER_MINUTE}/minute")
async def query_email(request: Request, email: str):
    session = SessionLocal()
    try:
        res = session.query(NameNum).filter(NameNum.email.like(f"%{email}%")).order_by(NameNum.name).all()
        return [row.__dict__ for row in res]
    finally:
        session.close()

@app.delete("/delete/")
@limiter.limit(f"{REQUESTS_PER_MINUTE}/minute")
async def delete_record(request: Request, name: str):
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
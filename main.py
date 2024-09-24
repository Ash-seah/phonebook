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
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_number = Column(String, index=True)
    email = Column(String, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    session = SessionLocal()
    try:
        res = session.execute(select(NameNum)).scalars().all()
        return [row.__dict__ for row in res]
    finally:
        session.close()

#TODO make this happen in SQL --DONE
#TODO
@app.put("/")
async def add_record(name:str, number:str):
    engine.execute(text(f'INSERT INTO name_num(name, phone_number) VALUES (\'{name}\', {number})'))

@app.get("/query/name/")
async def query_name(name:str):
    res = engine.execute(text(f'SELECT * FROM name_num HAVING LOWER(name) LIKE \'%{name.lower()}%\''))
    rows = []
    for row in res.mappings():
        rows.append(row)
    return str('\n'.join(str(v) for v in rows))

@app.get("/query/number/")
async def query_number(number:str):
    res = engine.execute(text(f'SELECT * FROM name_num WHERE phone_number LIKE \'%{number}%\''))
    rows = []
    for row in res.mappings():
        rows.append(row)
    return str('\n'.join(str(v) for v in rows))

@app.get("/query/email/")
async def query_number(email:str):
    res = engine.execute(text(f'SELECT * FROM name_num WHERE email LIKE \'%{email}%\''))
    rows = []
    for row in res.mappings():
        rows.append(row)
    return str('\n'.join(str(v) for v in rows))
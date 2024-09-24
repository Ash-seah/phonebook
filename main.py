import fastapi
import generate_random_data
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    res = engine.execute(text(f'SELECT * FROM name_num'))
    rows = []
    for row in res.mappings():
        rows.append(row)
    return str('\n'.join(str(v) for v in rows))

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
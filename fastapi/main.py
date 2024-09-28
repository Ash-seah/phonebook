from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
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

class Record(BaseModel):
    name: str
    number: str
    email: str

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Initialize the limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)


@app.get("/")
@limiter.limit(f"{REQUESTS_PER_MINUTE}/minute")
async def root(request: Request):
    """

    function in response to an empty query. will return all available data in JSON format.

    :param request: request object
    :return: JSON format. list of dictionaries
    :rtype: list
    """

    session = SessionLocal()
    try:
        res = session.execute(select(NameNum).order_by(NameNum.name)).scalars().all()
        return [row.__dict__ for row in res]
    finally:
        session.close()

@app.put("/")
@limiter.limit(f"{REQUESTS_PER_MINUTE}/minute")
async def add_record(record: Record, request: Request):
    """
        Add a new record to the database.

        This function allows adding a new record with a name, phone number, and email.
        It commits the new record to the database and returns a success message.
        If, for some reason, an error occurs, it rolls back the session and raises an HTTPException.

        :param record: The record to be added, containing name, phone number, and email.
        :type record: Record
        :param request: The request object.
        :type request: Request
        :return: A message indicating the record was added successfully.
        :rtype: List[Dict[str, Any]]
        :raises HTTPException: If there is an error during the process of adding the record to the database or if requests limit is reached.

        :Example:

        >>> record = Record(name="John Doe", number="1234567890", email="john.doe@example.com")
        >>> add_record(record, request)
        {"message": "Record added successfully"}
        """
    session = SessionLocal()
    try:
        new_record = NameNum(name=record.name, phone_number=record.number, email=record.email)
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
    """
        Query names from the database that match the given name pattern.

        This endpoint allows querying the "name_num" table of the MySQL database for records that match the
        provided pattern. The results are ordered alphabetically by name.

        :param request: The request object.
        :type request: Request
        :param name: The name pattern to search for.
        :type name: str
        :return: A list of dictionaries representing the rows that match the query.
        :rtype: List[Dict[str, Any]]
        :raises HTTPException: If the request limit is exceeded.
        """

    session = SessionLocal()
    try:
        res = session.query(NameNum).filter(NameNum.name.ilike(f"%{name}%")).order_by(NameNum.name).all()
        return [row.__dict__ for row in res]
    finally:
        session.close()

@app.get("/query/number/")
@limiter.limit(f"{REQUESTS_PER_MINUTE}/minute")
async def query_number(request: Request, number: str):
    """
    Query the database for entries matching the given phone number.

    This endpoint allows querying the "name_num" table of the MySQL database for records that match the
    provided phone number pattern. The results are ordered alphabetically by name.

    :param request: The request object.
    :type request: Request
    :param number: The phone number to search for.
    :type number: str
    :return: A list of dictionaries representing the matching database entries.
    :rtype: List[Dict[str, Any]]
    """

    session = SessionLocal()
    try:
        res = session.query(NameNum).filter(NameNum.phone_number.like(f"%{number}%")).order_by(NameNum.name).all()
        return [row.__dict__ for row in res]
    finally:
        session.close()

@app.get("/query/email/")
@limiter.limit(f"{REQUESTS_PER_MINUTE}/minute")
async def query_email(request: Request, email: str):
    """
        Query the database for entries matching the given email address.

        This endpoint allows querying the "name_num" table of the MySQL database for records that match the
        provided email address pattern. The results are ordered alphabetically by name.

        :param request: The request object.
        :type request: Request
        :param email: The email address to search for.
        :type email: str
        :return: A list of dictionaries representing the matching database entries.
        :rtype: List[Dict[str, Any]]
    """
    session = SessionLocal()
    try:
        res = session.query(NameNum).filter(NameNum.email.like(f"%{email}%")).order_by(NameNum.name).all()
        return [row.__dict__ for row in res]
    finally:
        session.close()

@app.delete("/delete/")
@limiter.limit(f"{REQUESTS_PER_MINUTE}/minute")
async def delete_record(request: Request, name: str):
    """
        Delete a record from the database by name.

        This endpoint allows deleting the first record from the "name_num" table of the MySQL database that matches the
        provided name. If the record is found and deleted, a success message is returned. If the record is not found,
        an HTTP 404 error is raised.

        :param request: The request object.
        :type request: Request
        :param name: The name of the record to delete.
        :type name: str
        :return: A message indicating the result of the delete operation.
        :rtype: Dict[str, str]
        :raises HTTPException: If the record is not found.
        """
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

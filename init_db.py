from sqlalchemy import inspect
from sqlalchemy import text
from sqlalchemy import create_engine
import pandas as pd

def initialize():
    engine = create_engine("mysql+mysqlconnector://root:admin@localhost/phonebook").connect()

    init = {'name': [], 'phone_number': [], 'email':[]}
    phonebook_DF = pd.DataFrame(init)

    generate_random_data.generate_record(phonebook_DF, 100)
    print(phonebook_DF)

    phonebook_DF.to_sql('name_num', con=engine, if_exists='replace', index=False)
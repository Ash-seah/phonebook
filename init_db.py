from sqlalchemy import create_engine
import pandas as pd
import generate_random_data

engine = create_engine("mysql+mysqlconnector://root:admin@localhost/phonebook").connect()

def initialize():
    """
        Initialize the phonebook DataFrame and populate it with random data.

        This function creates an empty DataFrame with columns for names, phone numbers, and emails.
        It then generates 100 random records and adds them to the DataFrame.
        Finally, it prints the DataFrame and saves it to a SQL database using a sqlalchemy connection.
    """

    init = {'name': [], 'phone_number': [], 'email':[]}
    phonebook_DF = pd.DataFrame(init)

    generate_random_data.generate_record(phonebook_DF, 100)
    print(phonebook_DF)

    phonebook_DF.to_sql('name_num', con=engine, if_exists='replace', index=False)
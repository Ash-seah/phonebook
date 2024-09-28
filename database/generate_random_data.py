from names_generator import generate_name
import random

def generate_record(df, repetition_num):
    """
        Generate and add records to a pandas DataFrame using names_generator library.

        This function generates a specified number of records and adds them to the given DataFrame.
        Each record consists of a name, a random 7-digit number, and an email address.

        :param df: The DataFrame to which records will be added.
        :type df: pandas.DataFrame
        :param repetition_num: The number of records to generate.
        :type repetition_num: int

        :Example:

        >>> import pandas as pd
        >>> df = pd.DataFrame(columns=['Name', 'Number', 'Email'])
        >>> generate_record(df, 5)
        >>> print(df)
        0  John Doe  1234567  John_Doe@gmail.com
        1  Jane Doe  2345678  Jane_Doe@gmail.com
        2  ...
    """

    for i in range(repetition_num):
        name = generate_name(style='capital')
        df.loc[len(df.index)] = [name, str(random.randint(1000000, 9999999)), '_'.join(name.split(' ')) + '@gmail.com']
from names_generator import generate_name
import random

def generate_record(df, repetition_num):
    for i in range(repetition_num):
        name = generate_name(style='capital')
        df.loc[len(df.index)] = [name, str(random.randint(1000000, 9999999)), '_'.join(name.split(' ')) + '@gmail.com']
from datetime import datetime
from tabulate import tabulate
import pandas as pd


def print_date(*args, date=None):
    msg = ''
    for arg in args:
        msg += str(arg)
        
    if date == None:
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        print(f'[{dt}]', msg)
        return
    
    print(date.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], msg)

def print_df(df, *args):
    msg = ''
    for arg in args:
        msg += str(arg)
        
    print_date(msg)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def dict_to_df(_dict):
    columns = list(_dict.keys())
    df = pd.DataFrame(columns=columns)
    df = df.append(_dict, ignore_index=True)
    df.set_index(columns[0], inplace=True)
    
    return df
    
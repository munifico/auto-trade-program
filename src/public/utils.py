from datetime import datetime
from tabulate import tabulate
import pandas as pd
import json


def print_date(*args, date=None):
    msg = ''
    for arg in args:
        msg += str(arg)

    if date == None:
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        print(f'[{dt}]', msg)
        return

    print(date.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], msg)


def print_json(json_data, *args):
    msg = ''
    for arg in args:
        msg += str(arg)

    print_date(msg)
    print(json.dumps(json_data, indent=4, ensure_ascii=False))

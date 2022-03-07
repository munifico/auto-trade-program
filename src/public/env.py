from dotenv import load_dotenv
import os

load_dotenv()


def load_env():
    UPBIT_ACCESS = os.environ.get('UPBIT_ACCESS')
    UPBIT_SECRET = os.environ.get('UPBIT_SECRET')

    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')

    TICKER = os.environ.get('TICKER')
    START = os.environ.get('START')
    ELAPSE = os.environ.get('ELAPSE')

    return UPBIT_ACCESS, UPBIT_SECRET, AWS_ACCESS_KEY, AWS_SECRET_KEY, TICKER, START, ELAPSE

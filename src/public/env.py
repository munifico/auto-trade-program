from dotenv import load_dotenv
import os

load_dotenv()


def load_env():
    UPBIT_ACCESS = os.environ.get('UPBIT_ACCESS')
    UPBIT_SECRET = os.environ.get('UPBIT_SECRET')
    ALGORITHM = os.environ.get('ALGORITHM')
    TICKER = os.environ.get('TICKER')

    return UPBIT_ACCESS, UPBIT_SECRET, ALGORITHM, TICKER

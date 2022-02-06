from dotenv import load_dotenv
import os

load_dotenv()


def load_env():
    UPBIT_ACCESS = os.environ.get('UPBIT_ACCESS')
    UPBIT_SECRET = os.environ.get('UPBIT_SECRET')

    return UPBIT_ACCESS, UPBIT_SECRET

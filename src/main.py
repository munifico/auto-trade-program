from algorithm.vbs import Vbs
from dotenv import load_dotenv
import os
from vb import Vb

if __name__ == '__main__':
    load_dotenv()

    UPBIT_ACCESS = os.environ.get('UPBIT_ACCESS')
    UPBIT_SECRET = os.environ.get('UPBIT_SECRET')
    TICKER = os.environ.get('TICKER')
    START = os.environ.get('START')
    ELAPSE = os.environ.get('ELAPSE')

    vb = Vb(access=UPBIT_ACCESS, secret=UPBIT_SECRET,
            ticker=TICKER, start=START, elapse=ELAPSE)

    vb.run()

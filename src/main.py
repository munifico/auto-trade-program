
from public.env import load_env
from algorithms.vbs import Vbs


if __name__ == '__main__':
    UPBIT_ACCESS, UPBIT_SECRET = load_env()

    vbs_btc = Vbs(access=UPBIT_ACCESS, secret=UPBIT_SECRET, ticker='KRW-CHZ')

    vbs_btc.start()

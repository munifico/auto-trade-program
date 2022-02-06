import sys
from vbs import run as vbs_run

if __name__ == '__main__':
    ticker = sys.argv[1]
    if not ticker or ticker == None:
        print('티커를 입력하세요.')
        sys.exit(1)

    vbs_run(ticker)

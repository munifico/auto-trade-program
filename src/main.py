import sys
from public.env import load_env
from algorithms.vbs import Vbs


if __name__ == '__main__':
    UPBIT_ACCESS, UPBIT_SECRET = load_env()

    argvs = sys.argv
    algorithm = argvs[1]
    ticker = argvs[2]

    # 여러 알고리즘을 하나의 키로 동시에 돌리게 되면
    # 요청 제한에 걸릴 수도, 큐를 사용해야겠네

    if algorithm == 'vbs':
        vbs = Vbs(access=UPBIT_ACCESS, secret=UPBIT_SECRET, ticker=ticker)
        vbs.start()

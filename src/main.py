from algorithm.one_per_gap.one_per_gap import one_per_gap_start
from public.env import load_env
from algorithm.vbs import Vbs


if __name__ == '__main__':
    UPBIT_ACCESS, UPBIT_SECRET, ALGORITH, TICKER = load_env()

    # 여러 알고리즘을 하나의 키로 동시에 돌리게 되면
    # 요청 제한에 걸릴 수도, 큐를 사용해야겠네

    if ALGORITH == 'vbs':
        vbs = Vbs(access=UPBIT_ACCESS, secret=UPBIT_SECRET, ticker=TICKER)
        vbs.run()
    elif ALGORITH == 'one_per_gap':
        one_per_gap_start(access=UPBIT_ACCESS,
                          secret=UPBIT_SECRET, ticker=TICKER)

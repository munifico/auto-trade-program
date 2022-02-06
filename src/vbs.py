import time
from datetime import datetime
from myupbit import MyUpbit
from utils import print_date, dict_to_df, print_df
from dotenv import load_dotenv
import os

load_dotenv()
ACCESS = os.environ.get('ACCESS')
SECRET = os.environ.get('SECRET')


myupbit = MyUpbit(access=ACCESS, secret=SECRET)


def run(ticker):
    print_date('프로그램을 시작합니다.')

    myupbit.print_balances()
    myupbit.set_ticker(ticker)

    hold = False
    sold = False
    i = 0
    while True:
        t_now = datetime.now()
        t_buy = myupbit.t_start.replace(
            hour=10, minute=5, second=0, microsecond=0)
        t_sell = myupbit.t_next.replace(
            hour=9, minute=45, second=0, microsecond=0)
        t_exit = myupbit.t_next.replace(
            hour=9, minute=50, second=0, microsecond=0)

        # AM 10:05 ~ AM 09:45 : 매수
        # 몇시 이전에 매수 하지 못하면 탄력이 없는것으로 판단하는건 어떤가
        if not hold and t_buy < t_now < t_sell:
            if not myupbit.target_price:
                myupbit.set_target_price_vbs()

            current_price = myupbit.get_current_price()

            if current_price > myupbit.target_price:
                res = myupbit.buy_market_order()

                if res:
                    hold = True

        # AM 09:45 ~ AM 09:50 : 매도
        if hold and not sold and t_sell < t_now < t_exit:
            res = myupbit.sell_market_order()

            if res:
                hold = False
                sold = True

        if t_exit < t_now:
            break

        if i == 180:
            current_price = myupbit.get_current_price()
            if not hold and not sold:
                status = '매수 대기 중'
            if hold:
                status = '매도 대기 중'
            if not hold and sold:
                status = '매도 완료'

            print_df(dict_to_df({'코인':  myupbit.ticker, '현재가': current_price,
                     '목표가': myupbit.target_price, '상태': status}), '현황')
            myupbit.print_balances()

            i = 0
        i += 1

        time.sleep(1)

    print_date('프로그램을 종료합니다.')
    myupbit.print_balances()

import warnings
from utils import dict_to_df, print_df, print_date
from datetime import datetime, timedelta
import pyupbit
import time
import pandas as pd
pd.options.display.float_format = '{:.5f}'.format
warnings.filterwarnings(action='ignore')


class MyUpbit:
    def __init__(self, access, secret):
        self.upbit = pyupbit.Upbit(access=access, secret=secret)
        self.t_start = datetime.now()
        self.t_prev = self.t_start - timedelta(days=1)
        self.t_next = self.t_start + timedelta(days=1)
        self.ticker = None
        self.target_price = None
        self.hold = False
        self.sold = False

    def print_balances(self):
        columns = ['자산', '보유수량', '평균매수가']
        balances = self.upbit.get_balances()
        df = pd.DataFrame(columns=columns)

        for balance in balances:
            df = df.append({'자산': balance['currency'], '보유수량': balance['balance'],
                            '평균매수가': balance['avg_buy_price']}, ignore_index=True)

        df.set_index('자산', inplace=True)
        print_df(df, '보유 자산')

    def set_ticker(self, ticker):
        self.ticker = ticker

    def get_ohlcv_base(self, base, days=200):
        df = pyupbit.get_ohlcv(
            ticker=self.ticker, interval="minute60", count=days*24)
        return df.resample('24H', base=base).agg({
            'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum', 'value': 'sum'
        })

    def set_target_price_vbs(self):
        print_date('[VBS] ', self.ticker, '의 목표가를 설정합니다.')
        df = self.get_ohlcv_base(base=10)
        df_today = df.loc[self.t_start.strftime('%Y-%m-%d 10:00:00')]
        df_yes = df.loc[self.t_prev.strftime('%Y-%m-%d 10:00:00')]

        range = df_yes['high'] - df_yes['low']
        self.target_price = df_today['open'] + range * 0.5

        print_date('[VBS] ', self.ticker, ' 목표가: ', self.target_price)

    def get_current_price(self, limit_info=False, verbose=False):
        return pyupbit.get_current_price(ticker=self.ticker, limit_info=limit_info, verbose=verbose)

    def buy_market_order(self):
        cash = self.upbit.get_balance()

        try:
            res = self.upbit.buy_market_order(self.ticker, cash * 0.9995)
            res_df = dict_to_df(res)
            print_df(res_df, self.ticker, ' 매수 주문 완료')

            time.sleep(1)

            while True:
                order = self.upbit.get_order(res['uuid'])

                if order != None and len(order['trades']) > 0:
                    order_df = dict_to_df(order)
                    volume = self.upbit.get_balance(self.ticker)

                    if volume == None:
                        continue

                    print_df(order_df, self.ticker,
                             '(', volume, ')', ' 매수 주문 처리 완료')
                    return True
                else:
                    print_df(self.ticker, ' 매수 주문 처리 대기 중...')
                    time.sleep(0.5)
        except:
            print_date(self.ticker, ' 매수 주문 실패')
            return False

    def sell_market_order(self):
        volume = self.upbit.get_balance(self.ticker)

        if volume == None:
            return False

        try:
            res = self.upbit.sell_market_order(self.ticker, volume)

            res_df = dict_to_df(res)
            print_df(res_df, self.ticker, ' 매도 주문 완료')

            time.sleep(1)

            while True:
                order = self.upbit.get_order(res['uuid'])
                if order != None and len(order['trades']) > 0:
                    order_df = dict_to_df(order)

                    cash = self.upbit.get_balance()

                    if cash == None:
                        continue

                    print_df(order_df, self.ticker, ' 매도 주문 처리 완료')
                    return True
                else:
                    print_df(self.ticker, ' 매수 주문 처리 대기 중...')
                    time.sleep(0.5)
        except:
            print_date(self.ticker, ' 매도 주문 실패')
            return False

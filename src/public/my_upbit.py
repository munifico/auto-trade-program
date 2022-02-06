import warnings
from public.utils import print_date, print_json
import pyupbit
import time
import pandas as pd
pd.options.display.float_format = '{:.5f}'.format
warnings.filterwarnings(action='ignore')


class MyUpbit(pyupbit.Upbit):
    def __init__(self, access, secret):
        pyupbit.Upbit.__init__(self, access=access, secret=secret)

    def _get_balances(self):
        balances = self.get_balances()
        out = []

        for balance in balances:
            out.append(
                {'자산': balance['currency'], '보유수량': balance['balance'], '평균매수가': balance['avg_buy_price']})

        return out

    def _get_ohlcv_base(self, ticker, base, days=200):
        df = pyupbit.get_ohlcv(
            ticker=ticker, interval="minute60", count=days*24)
        return df.resample('24H', base=base).agg({
            'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum', 'value': 'sum'
        })

    def _get_current_price(self, ticker, limit_info=False, verbose=False):
        return pyupbit.get_current_price(ticker=ticker, limit_info=limit_info, verbose=verbose)

    def _buy_market_order(self, ticker):
        cash = self.get_balance()
        if cash == None:
            raise Exception('잔고를 확인할 수 없습니다.')

        res = self.buy_market_order(ticker, cash * 0.9995)

        if res == None or 'error' in res:
            raise Exception()

        print_json(res, ticker, ' 매수 주문 완료')

        return res['uuid']

    def _check_buy_order(self, uuid, ticker):
        while True:
            order = self.get_order(uuid)

            if order != None and len(order['trades']) > 0:
                volume = self.get_balance(ticker)
                if volume == None:
                    continue

                print_json(order, ticker, '(', volume, ')', ' 매수 주문 처리 완료')
                break
            else:
                print_date(ticker, ' 매수 주문 처리 대기 중...')
                time.sleep(0.5)

    def _sell_market_order(self, ticker):
        volume = self.get_balance(ticker)
        if volume == None:
            raise Exception('보유 수량을 확인할 수 없습니다.')

        res = self.sell_market_order(ticker, volume)

        if res == None or 'error' in res:
            raise Exception()

        print_json(res, ticker, ' 매도 주문 완료')
        return res['uuid']

    def _check_sell_order(self, uuid, ticker):
        while True:
            order = self.get_order(uuid)

            if order != None and len(order['trades']) > 0:

                cash = self.get_balance()
                if cash == None:
                    continue

                print_json(order, ticker, '(', cash, ')', ' 매도 주문 처리 완료')
                break
            else:
                print_date(ticker, ' 매도 주문 처리 대기 중...')
                time.sleep(0.5)

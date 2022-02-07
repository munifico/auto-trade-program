import threading
import time
from public.my_upbit import MyUpbit
from public.utils import print_date, print_json
from collections import deque


class Consumer(MyUpbit, threading.Thread):
    def __init__(self, access, secret, ticker, q):
        threading.Thread.__init__(self)
        MyUpbit.__init__(self, access, secret)

        self.ticker = ticker
        self.q = q
        self.open_price = None
        self.current_price = None
        self.buy_price = None
        self.sell_price = None

        self.ma15 = deque(maxlen=15)
        self.ma50 = deque(maxlen=50)
        self.ma120 = deque(maxlen=120)

        df = self._get_ohlcv(ticker=self.ticker, interval="minute1")
        self.ma15.extend(df['close'])
        self.ma50.extend(df['close'])
        self.ma120.extend(df['close'])

        self.moving_avg = self.set_moving_avg()

        self.hold = False
        self.wait = False

    def run(self):
        print_date('[OPG] ', self.ticker, ' 프로그램을 시작합니다.')

        i = 0
        # 1분 마다
        while True:
            if not self.q.empty():
                self.open_price = self.q.get()
                self.set_moving_avg(self.open_price)

                # 보유하고 있지 않으면
                if self.hold == False:
                    self.buy_price = self._get_tick_size(
                        self.open_price * 1.01)
                    self.sell_price = self._get_tick_size(
                        self.open_price * 1.02)

                    self.wait = False

            self.current_price = self._get_current_price(ticker=self.ticker)

            # 매수 후 목표 가격에 매도 주문
            if not self.hold and not self.wait \
                    and self.moving_avg \
                    and self.current_price >= self.buy_price:
                try:
                    uuid = self._buy_market_order(ticker=self.ticker)
                    time.sleep(1)
                    self._check_buy_order(uuid=uuid, ticker=self.ticker)

                    uuid = self._sell_limit_order(
                        ticker=self.ticker, price=self.sell_price)
                    time.sleep(1)

                    self.hold = True
                except Exception as e:
                    print_date('[OPG] ', self.ticker, ' 매수 실패', e)

            # 매도
            if self.hold:
                res = self._check_sell_order(
                    uuid=uuid, ticker=self.ticker, loop=False)

                if res:
                    self.hold = False
                    self.wait = True

            if i == 10:
                print_json(self.get_ststus())
                i = 0
            i += 1

            time.sleep(1)

    def set_moving_avg(self, price=None):
        if price != None:
            self.ma15.append(price)
            self.ma50.append(price)
            self.ma120.append(price)

        ma15 = sum(self.ma15) / len(self.ma15)
        ma50 = sum(self.ma50) / len(self.ma50)
        ma120 = sum(self.ma120) / len(self.ma120)

        self.moving_avg = ma15 >= ma50 and ma15 <= ma50 * 1.03 and ma50 >= ma120

    def get_ststus(self):
        if not self.hold and not self.wait:
            status = '매수 대기 중'
        if self.hold and not self.wait:
            status = '매도 대기 중'
        if self.hold and self.wait:
            status = '다음 1분 기다리는 중'

        return {'[OPG]': self.ticker, '시작가': self.open_price, '현재가': self.current_price, '매수가': self.buy_price, '매도가': self.sell_price, '상태': status}

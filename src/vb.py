import time
from public.my_upbit import MyUpbit
from datetime import datetime, timedelta
from public.my_upbit import MyUpbit
from public.utils import print_date, print_json


class Vb(MyUpbit):
    def __init__(self, access, secret, ticker, start, elapse):
        MyUpbit.__init__(self, access, secret)

        self.ticker = ticker
        self.start = int(start)
        self.elapse = int(elapse)

        self.is_set_time = False
        self.is_set_target_price = False
        self.is_hold = True
        self.is_sell = False

    def run(self):
        # 프로그램 계속 시작 플래그
        print_date(self.ticker, ' 프로그램을 시작합니다.')

        if not self.is_set_time:
            self.set_time()

        self.set_target_price()

        i = 0
        while True:
            t_now = datetime.now()

            if not self.is_hold and self.t_buy < t_now < self.t_sell:
                if not self.is_set_target_price:
                    self.set_target_price()

                current_price = self._get_current_price(ticker=self.ticker)
                if current_price > self.target_price:
                    self.buy()

            if self.is_hold and not self.is_sell and t_now > self.t_sell:
                self.sell()

            # 프로그램 중단 플래그
            if t_now > self.t_exit:
                break

            if i == 180:
                i = 0
                self.print_status()

            i += 1
            time.sleep(1)

    def set_time(self):
        t_now = datetime.now()
        self.t_buy = t_now.replace(hour=self.start,
                                   minute=5, second=0, microsecond=0)

        # 프로그램 시작 시간 허용 한도
        # if t_now > self.t_buy + timedelta(minutes=25):
        # if t_now > self.t_buy:
        if t_now > self.t_buy + timedelta(hours=1):
            self.t_buy += timedelta(days=1)

        self.t_sell = self.t_buy + timedelta(hours=self.elapse-1, minutes=45)
        self.t_exit = self.t_sell + timedelta(minutes=5)

        self.is_set_time = True

        print_date(self.ticker, ' 매수 시간: ', self.t_buy,
                   ', 매도 시간: ', self.t_sell)

    def set_target_price(self):  # start 넘어서 진행한다.
        previous_date = self.t_buy - \
            timedelta(days=1, minutes=5) + timedelta(hours=self.elapse)
        df_previous = self._get_ohlcv_range_base(
            ticker=self.ticker, date=previous_date, start=self.start, elapse=self.elapse)

        df_current = self._get_ohlcv(
            ticker=self.ticker, interval="minute60", count=1)

        data_previous = df_previous.iloc[0, :]
        data_current = df_current.iloc[0, :]

        open = data_previous['open']
        high = data_previous['high']
        low = data_previous['low']
        close = data_previous['close']

        range = high - low
        noise = 1 - abs(open - close) / (high - low)  # 최근 n개의 평균을 내보는것도 시도

        self.target_price = range * noise + data_current['open']

        self.is_set_target_price = True

        print_date(self.ticker, ' 목표가: ', self.target_price)

    def buy(self):
        try:
            # 얼마나 분산 할 건지
            uuid = self._buy_market_order(ticker=self.ticker, ratio=1)
            time.sleep(1)
            self._check_buy_order(uuid=uuid, ticker=self.ticker)

            self.is_hold = True
        except Exception as e:
            print_date(self.ticker, ' 매수 실패', e)

    def sell(self):
        try:
            uuid = self._sell_market_order(ticker=self.ticker)
            time.sleep(1)
            self._check_sell_order(uuid=uuid, ticker=self.ticker)

            self.is_sell = True
            self.is_hold = False
        except Exception as e:
            print_date(self.ticker, ' 매도 실패', e)

    def get_status(self):  # 상태 조회
        current_price = self._get_current_price(ticker=self.ticker)
        if not self.is_hold and not self.is_sell:
            status = '매수 대기 중'
        if self.is_hold:
            status = '매도 대기 중'
        if not self.is_hold and self.is_sell:
            status = '매도 완료'

        return {'코인':  self.ticker, '현재가': current_price, '목표가': self.target_price, '상태': status}

    def print_status(self):  # 상태 출력
        status = self.get_status()
        balances = self._get_balances()

        print_json({
            '알고리즘': 'VBS',
            '현황': status,
            '잔고': balances
        }, '현재상태')

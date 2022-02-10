import time
from public.my_upbit import MyUpbit
from datetime import datetime, timedelta
from public.utils import print_date, print_json


class Vbs(MyUpbit):
    def __init__(self, access, secret, ticker):
        MyUpbit.__init__(self, access, secret)

        self.t_start = datetime.now()
        self.t_prev = self.t_start - timedelta(days=1)
        self.t_next = self.t_start + timedelta(days=1)

        self.ticker = ticker
        self.target_price = None

        self.hold = False
        self.sold = False

    def run(self):
        print_date('[VBS] ', self.ticker, ' 프로그램을 시작합니다.')
        t_buy = self.t_start.replace(
            hour=10, minute=5, second=0, microsecond=0)
        t_sell = self.t_next.replace(
            hour=9, minute=45, second=0, microsecond=0)
        t_exit = self.t_next.replace(
            hour=9, minute=50, second=0, microsecond=0)

        ticker_balance = self._get_balance(ticker=self.ticker)
        if ticker_balance != 0:
            self.hold = True
            self.sold = False

        i = 0
        while True:
            t_now = datetime.now()

            # AM 10:05 ~ AM 09:45 : 매수
            # 몇시 이전에 매수 하지 못하면 탄력이 없는것으로 판단하는건 어떤가
            if not self.hold and t_buy < t_now < t_sell:
                try:
                    if self.target_price == None:
                        self.set_target_price()

                    current_price = self._get_current_price(
                        ticker=self.ticker)

                    if current_price > self.target_price:
                        uuid = self._buy_market_order(ticker=self.ticker)
                        time.sleep(1)
                        self._check_buy_order(
                            uuid=uuid, ticker=self.ticker)

                        self.hold = True
                except Exception as e:
                    print_date('[VBS] ', self.ticker, ' 매수 실패', e)

            # AM 09:45 ~ AM 09:50 : 매도
            if self.hold and not self.sold and t_sell < t_now < t_exit:
                try:
                    uuid = self._sell_market_order(ticker=self.ticker)
                    time.sleep(1)
                    self._check_sell_order(uuid=uuid, ticker=self.ticker)

                    self.hold = False
                    self.sold = True
                except:
                    print_date('[VBS] ', self.ticker, ' 매도 실패', e)

            if t_exit < t_now:
                break

            if i == 180:
                i = 0
                self.print_status()

            i += 1
            time.sleep(1)

        print_date('[VBS] ', self.ticker, '프로그램을 종료합니다.')
        print_json(self._get_balances(), '잔고')

    def set_target_price(self):
        print_date('[VBS] ', self.ticker, '의 목표가를 설정합니다.')
        df = self._get_ohlcv_base(ticker=self.ticker, base=10)
        df_today = df.loc[self.t_start.strftime('%Y-%m-%d 10:00:00')]
        df_yes = df.loc[self.t_prev.strftime('%Y-%m-%d 10:00:00')]

        range = df_yes['high'] - df_yes['low']
        self.target_price = df_today['open'] + range * 0.5

        print_date('[VBS] ', self.ticker, ' 목표가: ', self.target_price)

    def get_status(self):
        current_price = self._get_current_price(ticker=self.ticker)
        if not self.hold and not self.sold:
            status = '매수 대기 중'
        if self.hold:
            status = '매도 대기 중'
        if not self.hold and self.sold:
            status = '매도 완료'

        return {'코인':  self.ticker, '현재가': current_price, '목표가': self.target_price, '상태': status}

    def print_status(self):
        status = self.get_status()
        balances = self._get_balances()

        print_json({
            '알고리즘': 'VBS',
            '현황': status,
            '잔고': balances
        }, '현재상태')

import threading
import time
from public.my_upbit import MyUpbit
from public.utils import print_date

class Producer(MyUpbit, threading.Thread):
    def __init__(self, access, secret, ticker, q):
        threading.Thread.__init__(self)
        MyUpbit.__init__(self, access, secret)
        
        self.ticker = ticker
        self.q = q
           
        
    def run(self):
        print_date('[OPG] ', self.ticker, ' 1분마다 검색을 시작합니다.')
        
        while True:            
            price = self._get_current_price(ticker=self.ticker)            
            self.q.put(price)
            time.sleep(60)
            
    
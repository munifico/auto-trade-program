import time
import threading
import queue
from collections import deque

import pyupbit
import datetime
from pyupbit import get_current_price, get_tickers, get_ohlcv
import pandas as pd
import warnings
warnings.filterwarnings(action='ignore')
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
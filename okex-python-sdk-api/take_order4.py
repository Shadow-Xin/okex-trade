import datetime
import time
from Tradin import Tradings
import logging

#下单数量
amount = 15
lowest = 20000
highest = 0
def take_order():
    global lowest
    global highest
    #输出当前时间
    print(datetime.datetime.now())
    take = Tradings()
    #全部撤单
    take.cancel_order()
    long_amount,short_amount,long_qty,short_qty,long_ratio,short_ratio,long_pnl,short_pnl = take.get_position()
    df = take.get_kline()
    #最后一个diff快线值和dea慢线值
    l_dif = df['dif'].values[-2]
    l_dea = df['dea'].values[-2]
    #最高价、最低价
    high = df['high'].values[-2]
    low = df['low'].values[-2]
    close = df['close'].values[-2]
    #上轨、下轨
    upper_band = df['upper_band'].values[-3]
    lower_band = df['lower_band'].values[-3]
#策略
    if l_dea > 0:
        print('上涨趋势')
        print('当前最低价：',df['low'].values[-2])
        print('当前收盘价：',df['close'].values[-2])
        print('当前上轨：',upper_band)
        print('当前下轨：',lower_band)
        if low < lowest :
            lowest = low
            print('上涨趋势历史最低价变更为：',lowest)
        if close > upper_band and l_dif > 0:
            print('上涨趋势，突破上轨，开多')
            if float(long_amount) == 0:
                print('暂未持多，开多：',amount)
                take.order_up(amount)
            if float(long_amount) == amount:
                print('已经持多：',long_amount)
            if float(long_amount) > 0 and float(long_amount) < amount:
                print('已经持多：',long_amount,'开多：',int(amount-int(long_amount)))
                take.order_up(int(amount-int(long_amount)))
        if float(long_amount) > 0:
            if close < lower_band:
                take.order_close_up(long_amount) 
                print('突破下轨，平多：',long_amount)
            if close < lowest:
                take.order_close_up(long_amount)
                print('跌破上升趋势以来最低价，平多：',long_amount)
        highest = 0
        if float(short_amount) > 0:
            take.order_close_down(short_amount)
            print('进入上涨趋势，平空：',short_amount)
                             

    if l_dea < 0:
        print('下跌趋势')
        print('当前最低价：',low)
        print('当前收盘价：',close)
        print('当前上轨：',upper_band)
        print('当前下轨：',lower_band)
        if high > highest :
            highest = high
            print('下涨趋势历史最低高价变更为：',lowest)
        if close < lower_band and l_dif < 0:
            print('下跌趋势，突破下轨，开空')
            if float(short_amount) == 0:
                print('暂未持空，开空：',amount)
                take.order_down(amount)
            if float(short_amount) == amount:
                print('已经持多：',short_amount)
            if float(short_amount) > 0 and float(short_amount) < amount:
                print('已经持空：',short_amount,'开空：',int(amount-int(short_amount)))
                take.order_down(int(amount-int(short_amount)))
        if float(short_amount) > 0:
            if close > upper_band:
                take.order_close_down(short_amount) 
                print('突破上轨，平空：',short_amount)
            if close < highest:
                take.order_close_down(short_amount)
                print('突破下跌趋势以来最高价，平空：',short_amount)
        lowest = 20000
        print(lowest)
        if float(long_amount) > 0:
            take.order_close_up(long_amount)
            print('进入下跌趋势，平多：',long_amount)


def get_now_time():
    now_second = datetime.datetime.now().second
    if now_second == 5:
        # print(now_second,'第5秒，运行macd策略')
        take_order()
    time.sleep(1)
while True:
    try:
        get_now_time()
    except Exception as e:
        logging.exception(e)
    


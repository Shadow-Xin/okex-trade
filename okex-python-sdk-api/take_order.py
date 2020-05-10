import datetime
import time
from Trading import Tradings
import logging

#下单数量
amount = 15

def take_order():
    #输出当前时间
    print(datetime.datetime.now())
    take = Tradings()
    #全部撤单
    take.cancel_order()
    long_amount,short_amount,long_qty,short_qty,long_ratio,short_ratio,long_pnl,short_pnl = take.get_position()
    df = take.get_kline()
    #最后一个dif快线值和dea慢线值
    l_dif = df['dif'].values[-1]
    l_dea = df['dea'].values[-1]
    if l_dea> 0:
        print('当前上涨趋势')
        if l_dif>l_dea:
            print('快线高于慢线')
            #上涨趋势，买入/持多
            if float(long_amount) > 0:
                print('持多:',long_amount)
            if float(long_amount) == 0:
                #开多
                take.order_up(amount)
            if float(short_amount) > 0:
                #平空
                take.order_close_down(short_amount)
            if float(short_amount) == 0:
                print('不持空')
        if l_dif<l_dea:
            print('快线低于慢线')
            if float(long_amount) > 0:
                #平多
                take.order_close_up(long_amount)
            if float(long_amount) == 0:
                print('不持多')
            if float(short_amount) > 0:
                print('持空:',short_amount)
            if float(short_amount) == 0:
                #开空
                take.order_down(amount)
    #下跌趋势
    if l_dea< 0:
        print('当前下跌趋势')
        if l_dif < l_dea:
            print('快线低于慢线')
            if float(short_amount) > 0:
                print('持空:',short_amount)
            if float(short_amount) == 0:
                #开空
                take.order_down(amount)
            if float(long_amount) >0:
                #平多
                take.order_close_up(long_amount)
            if float(long_amount) == 0:
                print('不持多')
        if l_dif>l_dea:
            print('快线高于慢线')
            if float(short_amount) > 0:
                #平空
                take.order_close_down(short_amount)
            if float(short_amount) == 0:
                print('不持空')
            if float(long_amount) >0:
                print('持多:',long_amount)
            if float(long_amount) == 0:
                #开多'
                take.order_up(amount)
    time.sleep(60)

while True:
    try:
        take_order()
    except Exception as e:
        logging.exception(e)
    


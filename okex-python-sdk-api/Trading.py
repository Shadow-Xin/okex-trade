#!/usr/bin/python
# -*- coding: utf-8 -*-
import okex.account_api as account
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import okex.index_api as index
import okex.option_api as option
import okex.system_api as system
import talib
import pandas as pd

api_key = "09e1d239-55bf-408a-9e25-907f1d9ed5e1"
secret_key = "40AD9FCCA7CA220693CBA1214CA1BB7D"
passphrase = "648464"
future_id = 'TBTC-USDT-200515'
futureAPI = future.FutureAPI(api_key, secret_key, passphrase, False)

class Tradings(object):

    def __init__(self):
        pass

    def order_up(self,amount):
        #开多
        price_depth = futureAPI.get_depth('BTC-USDT-200515', '2', '')
        buy_price = price_depth['bids'][1][0]
        order_result = futureAPI.take_order(instrument_id = future_id, type = '1',
        order_type='0',price = buy_price,size = str(amount),match_price = '0')
        print('开多:',amount)
    def order_down(self,amount):
        #开空
        price_depth = futureAPI.get_depth('BTC-USDT-200515', '2', '')
        sell_price = price_depth['asks'][1][0]
        order_result = futureAPI.take_order(instrument_id = future_id, type = '2',
        order_type='0',price = sell_price,size = str(amount),match_price = '0')
        print('开空:',amount)
    def order_close_up(self,long_amount):
        #平多
        price_depth = futureAPI.get_depth('BTC-USDT-200515', '2', '')
        sell_price = price_depth['asks'][1][0]
        order_result = futureAPI.take_order(instrument_id = future_id, type = '3',
        order_type='0',price = sell_price,size = long_amount,match_price = '0')
        print('平多:',long_amount)
    def order_close_down(self,short_amount):
        #平空
        price_depth = futureAPI.get_depth('BTC-USDT-200515', '2', '')
        buy_price = price_depth['bids'][1][0]
        order_result = futureAPI.take_order(instrument_id = future_id, type = '4',
        order_type='0',price = buy_price,size = short_amount,match_price = '0')
        print('平空:',short_amount)
    #撤单函数
    def cancel_order(self):
        # futureAPI = future.FutureAPI(api_key, secret_key, passphrase, False)
        #获取未成交和部分成交的订单列表
        order_list = []
        order_info = futureAPI.get_order_list(future_id, '0')[0]['order_info']
        for i in order_info:
            order_list.append(i['order_id'])
        order_info = futureAPI.get_order_list(future_id, '1')[0]['order_info']
        for i in order_info:
            order_list.append(i['order_id'])
        if order_list:
            canceled_orders = futureAPI.revoke_orders(future_id, order_ids=order_list)
            print('撤单成功')
        else:
            print('无单可撤')
    #获取仓位
    def get_position(self):
        #获取持仓
        holding_result = futureAPI.get_specific_position(future_id)
        # print(holding_result)
        #获取多仓可平仓数量，空仓可平仓数量
        long_amount = holding_result['holding'][0]['long_avail_qty']
        short_amount = holding_result['holding'][0]['short_avail_qty']
        #获取多仓数量、空仓数量
        long_qty = float(holding_result['holding'][0]['long_qty'])
        short_qty = float(holding_result['holding'][0]['short_qty'])
        #获取多仓收益率、空仓收益率
        long_ratio = float(holding_result['holding'][0]['long_pnl_ratio'])
        short_ratio = float(holding_result['holding'][0]['short_pnl_ratio'])
        #获取多仓收益、空仓收益
        long_pnl = float(holding_result['holding'][0]['long_pnl'])
        short_pnl = float(holding_result['holding'][0]['short_pnl'])
        print('多仓数量：',long_qty,'可平：',long_amount,'空仓数量：',short_qty,'可平：',short_amount)
        print('多仓收益：',long_pnl,'多仓收益率：',long_ratio)
        print('空仓收益：',short_pnl,'空仓收益率：',short_ratio)
        return long_amount,short_amount,long_qty,short_qty,long_ratio,short_ratio,long_pnl,short_pnl
    #获取行情
    def get_kline(self):
        k_result = futureAPI.get_kline('BTC-USDT-200515', '')
        df = pd.DataFrame(k_result,columns=['time','open','high','low','close','volume','vc'])
        df['dif'],df['dea'],df['hist'] = talib.MACD(df['close'].apply(float).values,fastperiod=12,
        slowperiod=26,signalperiod=9)
        return df

if __name__ == "__main__":
    take = Tradings()
    # take.order_up(15)
    # take.order_close_up(15)
    # take.order_down(15)
    # long_amount,short_amount,long_qty,short_qty,long_ratio,short_ratio,long_pnl,short_pnl = take.get_position()
    # print(long_amount,short_amount,long_qty,short_qty,long_ratio,short_ratio,long_pnl,short_pnl)
    df = take.get_kline()
    print(df)
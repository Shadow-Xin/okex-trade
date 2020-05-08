import okex.account_api as account
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import okex.index_api as index
import okex.option_api as option
import okex.system_api as system
import datetime
import pandas as pd
import talib
import time

api_key = "09e1d239-55bf-408a-9e25-907f1d9ed5e1"
secret_key = "40AD9FCCA7CA220693CBA1214CA1BB7D"
passphrase = "648464"
future_id = 'TBTC-USDT-200515'
futureAPI = future.FutureAPI(api_key, secret_key, passphrase, False)

#撤单函数
def cancel_order():
    futureAPI = future.FutureAPI(api_key, secret_key, passphrase, False)
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

#交易函数
def trades():
    print(datetime.datetime.now())
    cancel_order()
    #获取持仓
    holding_result = futureAPI.get_specific_position(future_id)
    # print(holding_result)
    #获取多仓可平仓数量，空仓可平仓数量
    long_amount = float(holding_result['holding'][0]['long_avail_qty'])
    short_amount = float(holding_result['holding'][0]['short_avail_qty'])
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
    k_result = futureAPI.get_kline('BTC-USDT-200515', '')
    df = pd.DataFrame(k_result,columns=['time','open','high','low','close','volume','vc'])
    upper_band, middle_band, lower_band = talib.BBANDS(df['close'].apply(float).values, timeperiod = 20, nbdevup = 2, nbdevdn = 2)
    pre_close_price = float(df['close'].values[-1])
    print(pre_close_price,upper_band[-1],lower_band[-1])

    #止盈止损部分
    #多仓平多止盈
    if long_amount > 0 and long_ratio >0.06:
        price_depth = futureAPI.get_depth('BTC-USDT-200515', '2', '')
        sell_price = price_depth['asks'][1][0]
        order_result = futureAPI.take_order(instrument_id = future_id, type = '3',
        order_type='0',price = sell_price,size = long_amount,match_price = '0')
        print('多仓平多止盈')
    #空仓平空止盈
    if short_amount > 0 and short_ratio >0.06:
        price_depth = futureAPI.get_depth('BTC-USDT-200515', '2', '')
        buy_price = price_depth['bids'][1][0]
        order_result = futureAPI.take_order(instrument_id = future_id, type = '4',
        order_type='0',price = buy_price,size = short_amount,match_price = '0')
        print('空仓平空止盈')
    #多仓平多止损
    if long_amount > 0 and long_ratio < -0.03:
        price_depth = futureAPI.get_depth('BTC-USDT-200515', '2', '')
        sell_price = price_depth['asks'][1][0]
        order_result = futureAPI.take_order(instrument_id = future_id, type = '3',
        order_type='0',price = sell_price,size = long_amount,match_price = '0')
        print('多仓平多止损')
    #空仓平空止损
    if short_amount > 0 and short_ratio < -0.03:
        price_depth = futureAPI.get_depth('BTC-USDT-200515', '2', '')
        buy_price = price_depth['bids'][1][0]
        order_result = futureAPI.take_order(instrument_id = future_id, type = '4',
        order_type='0',price = buy_price,size = short_amount,match_price = '0')
        print('空仓平空止损')

    #交易部分
    amount = 15 
    if pre_close_price > upper_band[-1]:
        print('超出上轨')
        if long_amount > 0 and short_amount > 0:
            price_depth = futureAPI.get_depth('BTC-USDT-200515', '2', '')
            buy_price = price_depth['bids'][1][0]
            order_result = futureAPI.take_order(instrument_id = future_id, type = '4',
            order_type='0',price = buy_price,size = short_amount,match_price = '0')
            print('有空有多，平空持多，持有多仓：',long_amount)
        if short_amount > 0 and long_amount == 0:
            price_depth = futureAPI.get_depth('BTC-USDT-200515', '2', '')
            #平空
            buy_price = price_depth['bids'][1][0]
            order_result = futureAPI.take_order(instrument_id = future_id, type = '4',
            order_type='0',price = buy_price,size = short_amount,match_price = '0')
            #开多
            order_result = futureAPI.take_order(instrument_id = future_id, type = '1',
            order_type='0',price = buy_price,size = str(amount),match_price = '0')
            print('有空无多，平空开多')
        if short_amount == 0 and long_amount > 0:
            print('无空有多，持有多仓：',long_amount)
        if short_amount == 0 and long_amount == 0:
            price_depth = futureAPI.get_depth('BTC-USDT-200515', '2', '')
            buy_price = price_depth['bids'][1][0]
            order_result = futureAPI.take_order(instrument_id = future_id, type = '1',
            order_type='0',price = buy_price,size = str(amount),match_price = '0')
            print('无空无多，买入开多')
    if pre_close_price < lower_band[-1]:
        print('低于下轨')
        if long_amount > 0 and short_amount > 0:
            #平多
            price_depth = futureAPI.get_depth('BTC-USDT-200515', '2', '')
            sell_price = price_depth['asks'][1][0]
            order_result = futureAPI.take_order(instrument_id = future_id, type = '3',
            order_type='0',price = sell_price,size = long_amount,match_price = '0')
            print('有多有空，平多持空，持有空仓：',short_amount)
        if long_amount > 0 and short_amount == 0:
            #平多
            price_depth = futureAPI.get_depth('BTC-USDT-200515', '2', '')
            sell_price = price_depth['asks'][1][0]
            order_result = futureAPI.take_order(instrument_id = future_id, type = '3',
            order_type='0',price = sell_price,size = long_amount,match_price = '0')
            #开空
            order_result = futureAPI.take_order(instrument_id = future_id, type = '2',
            order_type='0',price = sell_price,size = str(amount),match_price = '0')
            print('有多无空，平多开空')
        if long_amount == 0 and short_amount > 0:
            print('无多有空，持有空仓：',short_amount)
        if long_amount == 0 and short_amount == 0:
            price_depth = futureAPI.get_depth('BTC-USDT-200515', '2', '')
            sell_price = price_depth['asks'][1][0]
            order_result = futureAPI.take_order(instrument_id = future_id, type = '2',
            order_type='0',price = sell_price,size = str(amount),match_price = '0')
            print('无多无空，卖出开空')
    else:
        print('区间内运行')
    time.sleep(60)
while True:
    trades()

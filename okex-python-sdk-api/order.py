import okex.account_api as account
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import okex.index_api as index
import okex.option_api as option
import okex.system_api as system
import json
import datetime

def get_timestamp():
    now = datetime.datetime.now()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"

time = get_timestamp()

if __name__ == '__main__':

    api_key = "09e1d239-55bf-408a-9e25-907f1d9ed5e1"
    secret_key = "40AD9FCCA7CA220693CBA1214CA1BB7D"
    passphrase = "648464"
    future_id = 'TBTC-USD-200508'
    # param use_server_time's value is False if is True will use server timestamp

# 交割合约API
def trade():
    futureAPI = future.FutureAPI(api_key, secret_key, passphrase, False)
    # 单个合约持仓信息 （20次/2s）
    result = futureAPI.get_specific_position(future_id)
    #获取多仓可平仓数量，空仓可平仓数量
    long_amount = result['holding'][0]['long_avail_qty']
    short_amount = result['holding'][0]['short_avail_qty']
    amount = 1
    print(long_amount,short_amount)
    # 撤销未完成订单 （40次/2s）
    result = futureAPI.revoke_order(future_id, '')
    #向上击穿布林
    if pre_close_price > upper_band[-1]:
        #已经持有空仓
        if current_short > 0:
            #'买入平空' 
            #市价全平
            #order_result = futureAPI.close_position(future_id, 'short')
            order_result = futureAPI.take_order(instrument_id = future_id, type = '4',order_type='4',size = str(amount))
            print('已经已经持有空仓，买入平空')
        #并未持有多仓
        if current_long < amount:
            #'买入开仓'
            order_result = futureAPI.take_order(instrument_id = future_id, type = '1',order_type='4',size = str(amount))
            print('并未持有多仓，买入开仓')
    #向下击穿布林
    if pre_close_price < lower_band[-1]:
        #已经持有多仓
        if current_long > 0:
            #'卖出平多'
            #市价全平
            #order_result = futureAPI.close_position(future_id, 'long')
            order_result = futureAPI.take_order(instrument_id = future_id, type = '3',order_type='4',size = str(amount))
            print('已经持有多仓，卖出平多')
        #并未持有空仓
        if current_short < amount:
            #'卖出开空'
            order_result = futureAPI.take_order(instrument_id = future_id, type = '2',order_type='4',size = str(amount))
            print('并未持有空仓，卖出开空')
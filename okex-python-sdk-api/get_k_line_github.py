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
import pandas as pd
import datetime
import time
import pymysql
import logging

api_key = "09e1d239-55bf-408a-9e25-907f1d9ed5e1"
secret_key = "40AD9FCCA7CA220693CBA1214CA1BB7D"
passphrase = "648464"
future_id = 'TBTC-USDT-200626'
futureAPI = future.FutureAPI(api_key, secret_key, passphrase, False)


def get_k_line():
    k_result = futureAPI.get_kline('BTC-USDT-200626', '')
    df = pd.DataFrame(k_result,columns=['time','open','high','low','close','volume','vc'])
    #接收到的k线是逆序，新的数据在前面，改成顺序
    df = df.reindex(index=df.index[::-1])
    #时间格式由ISO 8601转为datetime
    df['time'] = df['time'].apply(lambda x :str(datetime.datetime(*time.strptime(x,'%Y-%m-%dT%H:%M:%S.%fZ')[:6])))
    #接收到的是字符串格式，转为数据
    df[['open','high','low','close','volume','vc']] = df[['open','high','low','close','volume','vc']].apply(pd.to_numeric)
    
    #写入数据库
    db = pymysql.connect("address","root","password","btc")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 插入语句
    sql = "INSERT IGNORE INTO btc(time,open,high,low,close,volume,vc) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    # 区别与单条插入数据，VALUES ('%s', '%s',  %s,  '%s', %s) 里面不用引号
    val = df[:299].values.tolist()
    cursor.executemany(sql,val)
    # 提交到数据库执行
    db.commit()
    # 关闭数据库连接
    db.close()
    print('success')
    time.sleep(17000)

while True:
    try:
        get_k_line()
    except Exception as e:
        logging.exception(e)
#dfdata/source/tushare/futures.py

import pandas as pd
import tushare as ts
from dfdata.source.tushare import default_config
from dfdata.util.func_tool import func_time
from dfdata.util.log import Log

log = Log()

pro = ts.pro_api()

# # 获取Tushare期货数据
# 期货数据接口：https://tushare.pro/document/2?doc_id=134  

@func_time
def get_futures_date(start_date='19901001', end_date=''):
    
    """
    在线获取Tushare交易日历
    
    返回DataFrame格式
    
    数据接口：https://tushare.pro/document/2?doc_id=137
    """
    
    #if start_date == '' : start_date='19901001'
    exchanges = list(default_config.futures_exchange.keys())
    result = pd.DataFrame(columns=['cal_date',])
    for exchange in exchanges:
        df = pro.trade_cal(exchange=exchange, start_date=start_date, end_date=end_date)
        #print(df.tail())
        df = df.rename(columns={'is_open':exchange})
        df = df[['cal_date', exchange]]
        result = pd.merge(result,df,on='cal_date',how='outer')
    result = result.sort_values(by='cal_date')
    
    #统一列名称
    result = result.rename(columns={'cal_date':'trade_date'})
    return result


@func_time
def get_futures_basic():
    """
    在线获取Tushare所有期货合约
    
    返回DataFrame格式
    
    数据接口：https://tushare.pro/document/2?doc_id=135
    """
    
    exchanges = default_config.futures_exchange  #tushare期货交易所字典 
    result =pd.DataFrame()
    for exchange, exchange_name in exchanges.items() :
        df = pro.fut_basic(exchange=exchange) 
        print("获取到{}的{}行合约数据".format(exchange_name, len(df)))
        result = pd.concat([result, df])
        
    #统一列名称
    result = result.rename(columns={'ts_code':'code'})
    return result

    
@func_time    
def get_futures_daily(trade_date):
    """
    在线获取一天Tushare期货的日行情数据
    
    返回DataFrame格式
    
    数据接口：https://tushare.pro/document/2?doc_id=138
    """    
    #获取一天数据
    df = pro.fut_daily(trade_date=trade_date)
    
    #统一列名称
    df = df.rename(columns={'ts_code':'code'})
    return df
    
    
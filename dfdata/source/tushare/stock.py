#dfdata/source/tushare/stock.py

import pandas as pd
import tushare as ts
from dfdata.source.tushare import default_config
from dfdata.util.func_tool import func_time
from dfdata.util.log import Log

log = Log()

pro = ts.pro_api()

@func_time
def get_stock_date(start_date='18000101', end_date=''):
    
    """
    在线获取Tushare交易日历
    
    返回DataFrame格式
    
    数据接口：https://tushare.pro/document/2?doc_id=26
    """
    
    exchanges = list(default_config.stock_exchange.keys())
    result = pd.DataFrame(columns=['cal_date',] )    
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
def get_stock_basic():
    """
    在线获取Tushare所有股票基本信息
    
    返回DataFrame格式
    
    数据接口：https://tushare.pro/document/2?doc_id=25
    """
    
    result =pd.DataFrame()
    for status, status_name in {'L':'上市','P':'暂停上市','D':'退市'}.items():
        df = pro.stock_basic(list_status=status, fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
        log.normal("获取到{}行{}的股票数据".format(len(df), status_name))
        result = pd.concat([result, df])
        
    #统一列名称
    result = result.rename(columns={'ts_code':'code', 
                                   'list_date':'start_date',
                                   'delist_date':'end_date',
                                   'list_status':'status'})
    return result


@func_time    
def get_stock_daily(trade_date):
    """
    在线获取一天Tushare股票的日行情数据
    
    返回DataFrame格式
    
    数据接口：https://tushare.pro/document/2?doc_id=27
    """    
    #获取一天数据
    df = pro.daily(trade_date=trade_date)
    
    #统一列名称
    df = df.rename(columns={'ts_code':'code'})
    return df
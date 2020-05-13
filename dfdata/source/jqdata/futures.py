#dfdata/source/jqdata/futures.py

import datetime
import time
import pandas as pd
import jqdatasdk as jq
from dfdata.util import config
from dfdata.util.func_tool import func_time
from dfdata.futures import read_futures_contract

#从配置文件读取账号密码，登录jqdata
user = config.get_config('jqdata','id')
password = config.get_config('jqdata','password')
jq.auth(user, password)
print('---登录jqdata----')
    
    
#获取最近一个交易日
def get_last_trade_date():
    today = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    last_trade_date_str = jq.get_trade_days(count=1,end_date=today)[0].strftime('%Y-%m-%d')
    return last_trade_date_str


@func_time
def get_futures_date(start_date='2005-01-01', end_date=''):
    """
    在线获取jqdata交易日历
    
    返回DataFrame格式
    
    数据接口：https://www.joinquant.com/help/api/help?name=JQData#get_trade_days-获取指定范围交易日
    jqdata数据从2005-01-01开始，
    
    
    """
    
    if start_date < '2005-01-01' : start_date='2005-01-01'
    trade_date_Series = jq.get_trade_days(start_date=start_date, end_date=end_date)
    df = pd.DataFrame(trade_date_Series,columns=['trade_date'])
    return df
 
    
@func_time
def get_futures_contract():
    """
    在线获取jqdata期货合约表
    
    返回DataFrame格式
    
    数据接口：https://www.joinquant.com/help/api/help?name=JQData#get_all_securities-获取所有标的信息
    截至2020年3月18日，jqdata中有期货合约数量5579
    """
    
    df_result = jq.get_all_securities(['futures'])
    df_result = df_result.reset_index()
    
    # 统一列名
    df_result = df_result.rename(columns={"index":"code",})
    
    # 将datetime类型转为字符串
    df_result["start_date"] = df_result["start_date"].apply(lambda x: x.strftime('%Y-%m-%d'))
    df_result["end_date"] = df_result["end_date"].apply(lambda x: x.strftime('%Y-%m-%d'))
   
    return df_result


@func_time
def get_futures_daily(trade_date):
    """
    在线获取jqdata日线行情
    
    返回DataFrame格式
    
    数据接口：get_price
    地址：https://www.joinquant.com/help/api/help?name=JQData#get_price-获取行情数据
    
    """   
    
    #获取一天数据
    
    sql = "SELECT code FROM futures_contract where start_date <= '{}' and end_date >= '{}' ".format(trade_date, trade_date)
    df_codes = read_futures_contract('jqdata', sql=sql, ) 
    codes = list(df_codes['code'])    #当天期货列表
    
    df = jq.get_price(
        codes, 
        start_date=trade_date,
        end_date=trade_date,
        frequency='daily', 
        fields=['open', 'close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit','low_limit', 'avg', 'pre_close', 'paused', 'open_interest'])
    
    if len(codes) != len(df) :
        raise Exception('{}当天期货获取不完整，期货{}个，获取到{}行'.format(trade_date, len(codes), len(df)))
    
    df["time"] = df["time"].apply(lambda x: x.strftime('%Y-%m-%d'))
    
    # 统一列名
    df = df.rename(columns={"time":"trade_date",})   
    
    return df


@func_time
def get_futures_min(trade_date, code):
    """
    在线获取jqdata分钟行情，一个合约一天分钟行情数据
    
    返回DataFrame格式
    
    数据接口：get_price
    地址：https://www.joinquant.com/help/api/help?name=JQData#get_price-获取行情数据
    
    """   
    #获取一个合约一天分钟行情数据
    df = jq.get_price(
        code,
        start_date=trade_date,
        end_date=datetime.datetime.strptime(trade_date, "%Y-%m-%d")+datetime.timedelta(days=1),
        frequency='1m', 
        fields=['open', 'close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit','low_limit', 'avg', 'pre_close', 'paused', 'open_interest'])
    
    df = df.reset_index()
    df["index"] = df["index"].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    df.insert(0, 'code', code)  #最前面插入一列code   
    
    # 统一列名
    df = df.rename(columns={"index":"date_time",})
     

    
   

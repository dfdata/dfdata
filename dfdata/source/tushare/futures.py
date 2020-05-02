#dfdata/source/tushare/futures.py

import time
import sqlite3
import pandas as pd
from dfdata.util.config import Config
from dfdata.util.func_tool import func_time
from dfdata.util.log import Log

pro = None
def auth():
    import tushare as ts
    global pro
    pro = ts.pro_api()

tushare_config = Config('tushare')

# # 下载Tushare期货数据
# 期货数据接口：https://tushare.pro/document/2?doc_id=134  
# 默认保存期货数据库futures_ts.db  


@func_time
def get_futures_date(start_date='19901001', end_date=''):
    
    """
    在线获取Tushare交易日历
    
    返回DataFrame格式
    
    数据接口：https://tushare.pro/document/2?doc_id=137
    """
    auth()
    
    #if start_date == '' : start_date='19901001'
    exchanges = list(tushare_config.exchange['futures'].keys())
    result = pd.DataFrame(columns=['date',])
    for exchange in exchanges:
        df = pro.trade_cal(exchange=exchange, start_date=start_date, end_date=end_date)
        #print(df.tail())
        df = df.rename(columns={'is_open':exchange, 'cal_date':'date'})
        df = df[['date', exchange]]
        result = pd.merge(df,result,on='date',how='outer')
    result = result.sort_values(by='date')
    
    return result


@func_time
def get_futures_contract():
    """
    在线获取Tushare所有期货合约
    
    返回DataFrame格式
    
    数据接口：https://tushare.pro/document/2?doc_id=135
    """
    auth()
    
    exchanges = tushare_config.exchange['futures']  #tushare期货交易所字典 
    df_result =pd.DataFrame()
    for exchange, exchange_name in exchanges.items() :
        df = pro.fut_basic(exchange=exchange) 
        print("获取到{}的{}行合约数据".format(exchange_name, len(df)))
        df_result = pd.concat([df_result, df])
    return df_result

    
@func_time    
def get_futures_daily():
    pass



def save_futures_daily_ts(
    db_name='data/futures_ts.db',
    table_name='futures_daily', 
    start_date='19960101', 
    end_date=''
):
    """
    保存期货日线行情表 save_ts_fut_daily
    期货日线行情表fut_daily，数据开始月1996年1月，每日盘后更新
    tushare当前限制：每分钟最多调用120次，单次最大2000条，总量不限制。
    通过交易日历获取所有要下载交易日
    -----
    参数：
    db_name 设置数据库名称，
    table_name 数据表名称
    start_date 下载开始时间
    end_date 下载结束时间
    -----
    返回值：
    
    
    -----
    示例：
    
    """
    exchanges = list(consts.EXCHANGE_NAME.keys())  #交易所列表，['CZCE', 'SHFE', 'DCE', 'CFFEX', 'INE'] 
    end_date = input_parser.end_date_parser(end_date)
    print(end_date)
    print(type(end_date))
    start_date = start_date  #下载开始时间
    print("开始下载日期："+start_date)
    print("结束下载日期："+end_date)  
    conn = input_parser.db_name_save_parser(db_name)

    
    #数据库已有日期集合
    try:
        sql = "select trade_date from {} ;".format(table_name)
        #默认：select trade_date from fut_daily
        df_trade_data = pd.read_sql_query(sql, conn) #获取数据库中trade_date列
        trade_date_in_db = set(df_trade_data['trade_date'])  #数据库中已有日期集合
    except:
        trade_date_in_db = set()  #如果数据表不存在，就设置已有日期为空集合
    print("数据库中已有交易日数量："+str(len(trade_date_in_db)))
     
    #要下载的交易日集合
    trade_date_all = set()  
    for exchange in exchanges:
        df = pro.trade_cal(exchange=exchange, start_date=start_date, end_date=end_date)
        df_set = set(df[df.is_open > 0 ]['cal_date'])
        trade_date_all = trade_date_all | df_set
        print('该时段内，{}共有{}个交易日'.format(consts.EXCHANGE_NAME[exchange], len(df_set)))
    print("要下载交易日数量："+str(len(trade_date_all)))
    #print(trade_date_all)
    
    #未完成的下载交易日
    trade_date_unfinished = trade_date_all - trade_date_in_db      
    print("未完成的下载交易日："+str(len(trade_date_unfinished)))
    
    for trade_date in trade_date_unfinished:
        df = pro.fut_daily(trade_date=trade_date)
        print(trade_date+'当天获取到行数：'+str(len(df)))
        
        df.to_sql("fut_daily", conn, index=False, if_exists="append")
        print(trade_date+"当天数据，已保存到数据库！")
        
        time.sleep(0.51) #休息0.5s，因为限制1分钟120次
    
    conn.close()
    print("数据保存完成")

    
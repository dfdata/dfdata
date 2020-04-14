# coding: utf-8
import time
import sqlite3
import pandas as pd
import tushare as ts
import dfdata.source.tushare.consts as consts
import dfdata.util.input_parser as input_parser
from dfdata.util.source import Source
pro = ts.pro_api()

tushare_source = Source('tushare')

# # 下载Tushare期货数据
# 期货数据接口：https://tushare.pro/document/2?doc_id=134  
# 默认保存期货数据库futures_ts.db  

# -----------------------------------------------------------------------------
# 期货合约表futures_contract，
def save_futures_contract(
    db_name=None,
    table_name=None,
):
    """
    保存期货合约表fut_basic，全部历史合约
    
    """
    # 如果没输入就设置为默认值
    if db_name == None : db_name = tushare_source.db_name['futures_db_name']
    if table_name == None : table_name = tushare_source.table_name['futures_contract']
    #检查值
    conn = input_parser.Connection_from_db_name(db_name)
    table_name = input_parser.check_table_name(table_name)
    print(db_name)
    exchanges = list(consts.EXCHANGE_NAME.keys())  #交易所列表，['CZCE', 'SHFE', 'DCE', 'CFFEX', 'INE'] 
    count = 0  #表的行数
    
    try:
        c = conn.cursor()
        c.execute('drop table {}'.format(table_name)) #删除数据库以前的fut_basic表
        print("删除之前{}表".format(table_name))
    except:
        pass
    
    for exchange in exchanges:
        df = pro.fut_basic(exchange=exchange) 
        print("获取到{}的{}行合约数据".format(consts.EXCHANGE_NAME[exchange], len(df)))
        df.to_sql(table_name, conn, index=False, if_exists="append")
        print("{}的合约数据，已保存到数据库！".format(consts.EXCHANGE_NAME[exchange]))
    
    
    conn.close()   #关闭数据库连接
    print("合约数据已全部保存！")


def read_futures_basic_ts():
    print('读取')
    
# -----------------------------------------------------------------------------
# 期货日线行情表 fut_daily

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

    
def save_futures_holding_ts():
    print("下载fut_holding")

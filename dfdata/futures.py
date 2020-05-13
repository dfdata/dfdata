#dfdata/futures.py

import importlib
import datetime
import time
import pandas as pd
from dfdata.util.config import KeyWords
import dfdata.util.db_tool as db_tool
from dfdata.util.log import Log
from dfdata.util.func_tool import func_time


#保存save_开头函数 ，调用数据源模块在线获取get_开头函数
#本地读取read_开头函数，调用数据源模块本地读取read_开头函数


################################################################################
### 期货日期表  futures_date
################################################################################

@func_time
def save_futures_date(
    source,
    **keywords
):   
    """   
    保存期货日期表
    
    输入数据源，默认保存该数据源期货日期表。

    Parameters
    ----------
    source : string
        数据源，如'tushare', 'jqdata'

    Returns
    -------
    None

    See Also
    --------
    read_futures_date : 读取期货日期表

    """
  
    #导入与数据源相应模块
    module_source_name = "dfdata.source."+source
    module_source = importlib.import_module(module_source_name)
    
    my_keywords = KeyWords(keywords, source_kind=source, data_kind='futures', table='futures_date')
    db =  my_keywords["db"]
    table =  my_keywords["table"]
    today_str = my_keywords['today']
    log_level = my_keywords['log']
    log = Log(log_level) #初始化log等级
    log.standard('normal', db=db, table=table, today=today_str) #打印参数
    
    #查询参数
    trade_date_name = 'trade_date'
  
    conn = db_tool.connection_from_db_name(db, save=True)
   
    ##查看数据库之前保存的时间，
    last_date_in_table_str=''
    next_date_in_table_str=''
    try:
        sql = "select {filed_name} from {table_name} order by {filed_name} desc limit 1;".format(filed_name=trade_date_name, table_name=table)
        log.debug("sql: " + sql)
        c = conn.cursor()
        result = c.execute(sql)
        last_dates = result.fetchone()
        last_date_in_table_str = last_dates[0]
        last_date = datetime.datetime.strptime(last_date_in_table_str, my_keywords.source.strftime_format)  
        next_date = last_date + datetime.timedelta(days=1)
        next_date_in_table_str = next_date.strftime(my_keywords.source.strftime_format)
        log.normal("数据库最后保存时间：" + last_date_in_table_str)
    except:
        pass
  
    
    if next_date_in_table_str <= today_str:
         #调用模块相应函数
        df = module_source.futures.get_futures_date(start_date=next_date_in_table_str, end_date=today_str)
        df.to_sql(table, conn, index=False, if_exists="append")
        log.normal("本次获取到{}行数据，已保存到{}表！".format(len(df), table))
    else:
        log.normal("{}表不需要更新，上次更新时间：{}".format(table, last_date_in_table_str))
    
    log.normal("操作完成。\n")
    
    db_tool.db_info(db, table=table, log_level=log_level)
        
    conn.close()
    
#函数，本地读取期货日期表   
read_futures_date = db_tool.return_function_read_data_in_db(data_kind='futures', data_table='futures_date')
  
    
################################################################################
### 期货合约表  futures_contract
################################################################################

@func_time  
def save_futures_contract(
    source,
    **keywords
):   
    """   
    保存期货合约表
    
    输入数据源，默认保存该数据源期货合约表。

    Parameters：
        source (str): 数据源名称
        db (str): 数据库名称
        
    Returns:
        None
        
    See Also：
        read_futures_contract()
        
    Notes:
        笔记
        
    Examples:
        save_futures_contract(source="tushare")
    """
    
    #导入与数据源相应模块
    module_source_name = "dfdata.source."+source
    module_source = importlib.import_module(module_source_name)

    #输入参数和默认参数
    my_keywords = KeyWords(keywords, source_kind=source, data_kind='futures', table='futures_contract')
    db =  my_keywords["db"]
    table =  my_keywords["table"]
    today_str = my_keywords['today']
    log_level = my_keywords['log']
    log = Log(log_level) #初始化log等级
    keywords['log'] = log
    log.standard('normal', db=db, table=table, today=today_str)
    log.info('log_level:'+log_level)

    
    conn = db_tool.connection_from_db_name(db, save=True)
    #今天时间，如：2020-03-18
    #today_str = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d')
    
    ##查看数据库之前保存的时间，
    update_date_in_table=''
    try:
        sql = "select update_date from {} limit 1;".format(table)
        c = conn.cursor()
        result = c.execute(sql)
        update_dates = result.fetchone()
        update_date_in_table = update_dates[0]
    except:
        pass
    
    if update_date_in_table == today_str:   #可以获取最近交易日last_trade_date_str
        log.normal("{}表已是最新, 上次时间为：{}".format(table, update_date_in_table))
    else:
        #调用模块相应函数，获取所有期货合约
        df = module_source.futures.get_futures_contract()
        df['update_date'] = today_str
        df.to_sql(table, conn, index=False, if_exists="replace")
        log.normal("一共获取到{}行数据，已保存到{}表".format(len(df), table))
    
    log.normal("操作完成。\n")
    conn.close()
    
    db_tool.db_info(db, table=table)    
    
#读取期货合约表函数
read_futures_contract = db_tool.return_function_read_data_in_db(data_kind='futures', data_table='futures_contract')


################################################################################
### 期货日行情表  futures_daily
################################################################################

@func_time
def save_futures_daily(
    source,
    **keywords
):  
    
    #导入与数据源相应模块
    module_source_name = "dfdata.source."+source
    module_source = importlib.import_module(module_source_name)

    #输入参数和默认参数
    my_keywords = KeyWords(keywords, source_kind=source, data_kind='futures', table='futures_daily')
    db =  my_keywords["db"]
    table =  my_keywords["table"]
    today_str = my_keywords['today']
    start_date = my_keywords['start_date']
    end_date = my_keywords['end_date']
    sleep_time = my_keywords['sleep_time']
    log_level = my_keywords['log']
    log = Log(log_level) #初始化log等级
    keywords['log'] = log
    log.standard('normal', db=db, table=table, today=today_str, start_date=start_date, end_date=end_date) #打印参数
    log.info('log_level:'+log_level)
     
    #要下载的交易日集合 all_trade_date_set = set()  
    #先更新日期表 save_futures_date  
    save_futures_date(source, db=db, log='warning') #log等级设置为warning，普通打印都不会显示
    all_trade_date = read_futures_date(source,  db=db, exchange='CZCE', start_date=start_date, end_date=end_date, is_open=1)
    all_trade_date_set = set(all_trade_date['trade_date'])
    log.normal("一共{}交易日的日行情数据需要下载".format(len(all_trade_date_set)))
   
    #数据库已有
    conn = db_tool.connection_from_db_name(db)   
    
    #数据库已有日期集合
    try:
        #read_futures_daily()
        trade_date_in_db = read_futures_daily(source, db=db, table=table, fields='trade_date', start_date=start_date, end_date=end_date,)
        trade_date_in_db_set = set(trade_date_in_db['trade_date'])
        log.normal("数据库中已有{}天日行情数据："+str(len(trade_date_in_db_set))) 
    except:
        trade_date_in_db_set = set() #如果数据表不存在，就设置已有日期为空集合
        log.normal("数据库中没有日行情数据。")
        
    """
    #直接查询
    try:
        sql = "select trade_date from {} WHERE start_date >= '{}' and end_date <= '{}';".format(table_name, start_date, end_date)
        df_date = pd.read_sql_query(sql, conn) #获取数据库中date列
        trade_date_in_db_set = set(df_trade_data['trade_date'])  #数据库中已有日期集合
        log.normal("数据库中已有{}天日行情数据："+str(len(trade_date_in_db_set)))
    except:
        trade_date_in_db_set = set()  #如果数据表不存在，就设置已有日期为空集合
        log.normal("数据库中没有日行情数据。")    
    """
    
    #未完成的下载交易日
    trade_date_unfinished = list(all_trade_date_set - trade_date_in_db_set)  
    #下载列表倒序，最近日期比之前日期更常用
    trade_date_unfinished.sort(reverse = True)
    log.normal("未完成下载的交易日数量："+str(len(trade_date_unfinished)))

    for trade_date in trade_date_unfinished: #如果集合中，有要下载的交易日
         #调用模块相应函数，获取所有期货合约
        df = module_source.futures.get_futures_daily(trade_date=trade_date)
        log.normal("{} 当天获取到{}行数据。".format(trade_date, str(len(df))))
        
        df.to_sql(table, conn, index=False, if_exists="append")
        
        time.sleep(sleep_time) #休息0.5s，因为限制1分钟120次
        
    conn.close()
    log.normal("日线行情数据保存完成。")        
    
    db_tool.db_info(db, table=table)

#读取期货日线表函数  futures_daily
read_futures_daily = db_tool.return_function_read_data_in_db(data_kind='futures', data_table='futures_daily')


################################################################################
### 期货分钟行情表  futures_min
################################################################################
@func_time
def save_futures_min(
    source,
    **keywords
):  
    #导入与数据源相应模块
    module_source_name = "dfdata.source."+source
    module_source = importlib.import_module(module_source_name)   
    
    #输入参数和默认参数
    my_keywords = KeyWords(keywords, source_kind=source, data_kind='futures', table='futures_min')
    db =  my_keywords["db"]
    table =  my_keywords["table"]
    today_str = my_keywords['today']
    start_date = my_keywords['start_date']
    end_date = my_keywords['end_date']
    sleep_time = my_keywords['sleep_time']
    log_level = my_keywords['log']
    log = Log(log_level) #初始化log等级
    keywords['log'] = log
    log.standard('normal', db=db, table=table, today=today_str, start_date=start_date, end_date=end_date) #打印参数
    log.info('log_level:'+log_level) 
    
    code =  my_keywords["code"]
    
    # 最后一个可能在当天没更新完整，单独更新
    # 
    try:
        sql = 'select * from futures_daily where trade_date = (select max(trade_date) from futures_daily)'
        df_last_date = da.read_futures_daily(source, db=db, table=table,sql=sql)
    except:
        pass
    
    #要下载的交易日集合
    all_trade_date = read_futures_date(source,  db=db, exchange='CZCE', start_date=start_date, end_date=end_date, is_open=1)
    all_trade_date_set = set(all_trade_date['trade_date'])   
    print("要下载交易日数量："+str(len(trade_date_all)))
       
    #数据库futures_min表code已有日期集合
    try:
        trade_date_in_db = read_futures_min(source, db=db, table=table, fields='trade_date', code=code)
        trade_date_in_db_set = set(trade_date_in_db['trade_date'])
        log.normal("数据库中已有{}天日行情数据："+str(len(trade_date_in_db_set))) 
    except:
        trade_date_in_db_set = set() #如果数据表不存在，就设置已有日期为空集合
        log.normal("数据库中没有日行情数据。")    
    
    #未完成的下载交易日
    trade_date_unfinished = trade_date_all - trade_date_in_db      
    print("未完成的下载交易日："+str(len(trade_date_unfinished)))
    unfinished_dates_sorted = list(trade_date_unfinished).sort(reverse=True) 
    
    for trade_date in trade_date_unfinished:    
         #调用模块相应函数，获取所有期货合约
        df = module_source.futures.get_futures_daily(trade_date=trade_date)
        log.normal("{} 当天获取到{}行数据。".format(trade_date, str(len(df))))        
        df.to_sql(table, conn, index=False, if_exists="append")    #存储到数据库  
        time.sleep(sleep_time)   #休息0.5s，因为限制1分钟120次    
        
    conn.close()
    print("数据保存完成")    
   

#读取期货日线表函数  futures_daily
read_futures_min = db_tool.return_function_read_data_in_db(data_kind='futures', data_table='futures_min')



    
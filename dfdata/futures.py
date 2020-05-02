import importlib
import datetime
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
  
    conn = db_tool.connection_from_db_name(db, save=True)
   
    ##查看数据库之前保存的时间，
    last_date_in_table_str=''
    next_date_in_table_str=''
    try:
        sql = "select date from {} order by date desc limit 1;".format(table)
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
    


@func_time   
def read_futures_date(
    source,
    **keywords
):
    """   
    本地读取期货日期表
    
    输入数据源，默认读取全部。

    Parameters：
        source (str): 数据源名称
        db (str): 数据库名称
        start_date: 
        end_date: 
        
    Returns:
        返回DataFrame格式的交易日
        
    See Also：
        save_futures_date()
        
    Notes:
        笔记
        
    Examples:
        read_futures_date("tushare")
    """
    
    #导入与数据源相应模块
    module_source_name = "dfdata.source."+source
    module_source = importlib.import_module(module_source_name)
    
    #输入参数和默认参数
    my_keywords = KeyWords(keywords, source_kind=source, data_kind='futures', table='futures_date')
    db =  my_keywords["db"]
    table =  my_keywords["table"]
    today_str = my_keywords['today']
    start_date = my_keywords['start_date']
    end_date = my_keywords['end_date']
    fields = my_keywords['fields']
    is_open = my_keywords['is_open']
    sql = my_keywords['sql']
    log_level = my_keywords['log']
    log = Log(log_level) #初始化log等级
    keywords['log'] = log
    log.standard('info', db=db, table=table, today=today_str, log_level=log_level)

    conn = db_tool.connection_from_db_name(db)
    
    if log_level in ['info', 'debug']: 
        db_tool.db_info(db, table=table, log_level=log_level)
    
    #数据库中获取数据
    if sql == None : #如果没输入sql语句，其他参数有效
        sql = "select {} from {} where date >= '{}' and  date <= '{}'".format(fields, table,start_date,end_date)
    log.info("sql语句："+sql)
    df = pd.read_sql_query(sql, conn)
    conn.close()
         
    return df    
    
    
    
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
    
@func_time      
def read_futures_contract(
    source,
    **keywords      
):
    """   
    读取期货合约表
    
    Parameters:
        code (str): 合约代码，默认None
        exchange (str): 交易所代码，默认None
    
    """   
    
    #输入参数和默认参数
    my_keywords = KeyWords(keywords, source_kind=source, data_kind='futures', table='futures_contract')
    db =  my_keywords["db"]
    table =  my_keywords["table"]
    today_str = my_keywords['today']
    log_level = my_keywords['log']
    log = Log(log_level) #初始化log等级
    
    #函数查询
    start_date = my_keywords['start_date']
    end_date = my_keywords['end_date']
    fields = my_keywords['fields']
    code = my_keywords['code'] 
    exchange = my_keywords['exchange']
    limit = my_keywords['limit']
    sql = my_keywords['sql']

    #打印参数
    log.standard('info', db=db, table=table, today=today_str, log_level=log_level) 

    conn = db_tool.connection_from_db_name(db)
    
    if log_level in ['info', 'debug']: 
        db_tool.db_info(db, table=table, log_level=log_level)
        
    where = db_tool.sql_where(has_where=True, operator='=', code=code, exchange=exchange)
    sql = db_tool.get_sql(sql=sql, fields=fields, table=table, where=where, limit=limit, log_level=log_level)
    
    df = pd.read_sql_query(sql, conn)
    
    conn.close()
    return df   


################################################################################
### 期货日线表  futures_daily
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
    log_level = my_keywords['log']
    log = Log(log_level) #初始化log等级
    keywords['log'] = log
    log.standard('normal', db=db, table=table, today=today_str) #打印参数
    log.info('log_level:'+log_level)
     
    #要下载的交易日集合
    all_trade_date_set = set()  
    all_trade_date = read_futures_date(source=source, db=db, table='futures_date', start_date=start_date,end_date=end_date)
   
    
    conn = db_tool.connection_from_db_name(db)      
    #数据库已有日期集合
    try:
        sql = "select date from {} ;".format(table_name)
        df_date = pd.read_sql_query(sql, conn) #获取数据库中date列
        date_in_db_set = set(df_trade_data['trade_date'])  #数据库中已有日期集合
        log.normal("数据库中已有{}天日行情数据："+str(len(trade_date_in_db)))
    except:
        date_in_db_set = set()  #如果数据表不存在，就设置已有日期为空集合
        log.normal("数据库中没有日行情数据。")    
    
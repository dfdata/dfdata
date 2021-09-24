
import pandas as pd
from dfdata.util.log import Log
from dfdata.util.config import KeyWords
from dfdata.util import db_tool
from dfdata.util.func_tool import func_time


def return_function_read_date_table(data_kind, data_func_name):
    """
    闭包，返回读取数据库函数
    
    参数：
    data_kind (str)：数据种类，如'futures'
    data_func_name (str) : 数据表名称，如'futures_date'
    
    示例：
    read_futures_date = return_function_read_date_table(data_kind='futures', data_func_name='futures_date')
    read_futures_date为一个函数，执行该函数里的read_date_table函数。
    """
    
    
    @func_time
    def read_date_table(source, **keywords):
        """   
        从数据库读取数据

        Parameters:
            # 通用参数
            source (str): 数据源名称
            db (str) : 数据库名称
            table (str) : 数据表名称
            log (str) : log等级，如info, debug等，默认normal,
            sql (str) : sql语句，如果sql有输入，只支持该查询语句。
            fields (str or tuple) : 显示字段
            limit (int or tuple) : 读取数量，如5, (5, 80)
            
            # 不固定参数
            start_date (str or int or datetime) : 开始时间
            code : 代码
            

        """   

        #输入参数和默认参数
        my_keywords = KeyWords(keywords, source_kind=source, data_kind=data_kind, data_func_name=data_func_name, function_kind='read')
        db =  my_keywords["db"]
        table =  my_keywords["table"]
        today_str = my_keywords['today']
        log_level = my_keywords['log']
        log = Log(log_level) #初始化log等级

        #函数查询， 默认参数
        start_date_input = my_keywords['start_date']
        end_date_input = my_keywords['end_date']
        code = my_keywords['code']
        fields = my_keywords['fields']
        is_open = my_keywords['is_open']
        exchange = my_keywords['exchange']
        trade_date = my_keywords['trade_date']
        limit = my_keywords['limit']
        sql = my_keywords['sql']

        #打印参数
        log.standard('info', db=db, table=table, today=today_str, log_level=log_level) 

        conn = db_tool.connection_from_db_name(db)

        if log_level in ['info', 'debug']: 
            db_tool.db_info(db, table=table, log_level=log_level)

        #日期表生成sql语句
        log.debug("日期表生成sql语句")

        if exchange != None:  #如果交易所参数有输入则只显示该列
            fields='trade_date, '+ exchange

        filter_is_open = db_tool.sql_filter(exchange, '=', is_open)
        filter_start_end_date_str = db_tool.sql_filter_start_end_date('trade_date', start_date_input, end_date_input)

        where = db_tool.sql_where(filter_start_end_date_str, filter_is_open) 

        search_sql = db_tool.get_sql(sql=sql, fields=fields, table=table, where=where, limit=limit, log_level=log_level)
        log.debug("sql：" + search_sql)
        df = pd.read_sql_query(search_sql, conn)

        #关闭连接，返回结果
        conn.close()     
        return df   
    
    #返回函数read_date_table
    return read_date_table


def return_function_read_normal_table(data_kind, data_func_name):
    """
    闭包，返回读取数据库函数
    
    参数：
    data_kind (str)：数据种类，如'futures'
    data_func_name (str) : 数据表名称，如'futures_date'
    
    示例：
    read_futures_basic = return_function_read_normal_table(data_kind='futures', data_func_name='futures_date')
    read_futures_basic为一个函数，执行该函数里的read_normal_table函数。
    """
    
    
    @func_time
    def read_normal_table(source, **keywords):
        """   
        从数据库读取数据

        Parameters:
            # 通用参数
            source (str): 数据源名称
            db (str) : 数据库名称
            table (str) : 数据表名称
            log (str) : log等级，如info, debug等，默认normal,
            sql (str) : sql语句，如果sql有输入，只支持该查询语句。
            fields (str or tuple) : 显示字段
            limit (int or tuple) : 读取数量，如5, (5, 80)
            
            # 不固定参数
            start_date (str or int or datetime) : 开始时间
            code : 代码
        
        """   

        #输入参数和默认参数
        my_keywords = KeyWords(keywords, source_kind=source, data_kind=data_kind, data_func_name=data_func_name, function_kind='read')
        db =  my_keywords["db"]
        table =  my_keywords["table"]
        today_str = my_keywords['today']
        log_level = my_keywords['log']
        log = Log(log_level) #初始化log等级

        #函数查询， 默认参数
        start_date_input = my_keywords['start_date']
        end_date_input = my_keywords['end_date']
        code = my_keywords['code']
        fields = my_keywords['fields']
        is_open = my_keywords['is_open']
        exchange = my_keywords['exchange']
        trade_date = my_keywords['trade_date']
        limit = my_keywords['limit']
        sql = my_keywords['sql']
         

        #打印参数
        log.standard('info', db=db, table=table, today=today_str, log_level=log_level) 

        conn = db_tool.connection_from_db_name(db)

        if log_level in ['info', 'debug']: 
            db_tool.db_info(db, table=table, log_level=log_level)

        log.debug("其他表生成生成sql语句")
        #生成where语句
        filter_normal = db_tool.sql_filters(operator='=', code=code, exchange=exchange, trade_date=trade_date)
        filter_start_end_date_str = db_tool.sql_filter_start_end_date('trade_date', start_date_input, end_date_input)   
        where = db_tool.sql_where(filter_normal, filter_start_end_date_str)

        #生成sql语句，如果有输入sql参数，sql语句就为输入语句。否则按fields，table，where，limit四部分生成。
        search_sql = db_tool.get_sql(sql=sql, fields=fields, table=table, where=where, limit=limit, log_level=log_level)
        log.debug("sql：" + search_sql)
        df = pd.read_sql_query(search_sql, conn)

        #关闭连接，返回结果
        conn.close()     
        return df   
    
    #返回函数read_normal_table
    return read_normal_table



################################################################################
### 期货函数  futures
################################################################################

#函数，本地读取期货日期表   
read_futures_date = return_function_read_date_table(data_kind='futures', data_func_name='futures_date')

#读取期货合约表函数
read_futures_basic = return_function_read_normal_table(data_kind='futures', data_func_name='futures_basic')

#读取期货日线表函数  futures_daily
read_futures_daily = return_function_read_normal_table(data_kind='futures', data_func_name='futures_daily')

#读取期货日线表函数  futures_daily
read_futures_min = return_function_read_normal_table(data_kind='futures', data_func_name='futures_min')



################################################################################
### 股票函数  stock
################################################################################

read_stock_date = return_function_read_date_table(data_kind='stock', data_func_name='stock_date')

read_stock_basic =  return_function_read_normal_table(data_kind='stock', data_func_name='stock_basic')

read_stock_daily = return_function_read_normal_table(data_kind='stock', data_func_name='stock_daily')



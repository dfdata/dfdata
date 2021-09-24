import sys
import importlib
import datetime
import time
import sqlite3
import pandas as pd
from dfdata.util.log import Log
from dfdata.util.config import KeyWords
from dfdata.util import db_tool
from dfdata.util.func_tool import func_time
from dfdata import read_data


#获取当前模块对象， 用于getattr()调用本模块函数。
this_module = sys.modules[__name__]

def return_function_save_by_once(
    data_kind,                         
    data_func_name,
):
    """
    闭包，返回函数save_by_once
    
    一次性保存数据：
    1.查看数据库字段update_date之前保存时间。
    2.判断保存时间是否小于最后交易日，小于就获取数据
    3.调用数据源对应函数，获取所有数据函数，get_{data_func_name}()。如：get_futures_basic()
    4.替换之前表格所有数据。
    
    参数：
    data_kind (str)：数据种类，如'futures'
    data_func_name (str) : 函数名称，如'futures_basic'
    
    示例：
    save_futures_basic = return_function_save_by_once(data_kind='futures', data_func_name='futures_basic')
    save_futures_basic为一个函数，执行该函数里的save_by_once函数。
    """    
    @func_time
    def save_by_once(source, **keywords):
    
        #导入与数据源相应数据类别模块
        module_name = "dfdata.source.{}.{}".format(source, data_kind)
        source_module = importlib.import_module(module_name)
        
        #获取数据函数的名称，如：'get_futures_basic'
        get_data_func_name = 'get_{}'.format(data_func_name)  

        #输入参数和默认参数
        my_keywords = KeyWords(keywords, source_kind=source, data_kind=data_kind, data_func_name=data_func_name)
        db =  my_keywords["db"]
        table =  my_keywords["table"]
        today_str = my_keywords['today']
        log_level = my_keywords['log']
        log = Log(log_level) #初始化log等级
        keywords['log'] = log
        log.standard('normal', db=db, table=table, today=today_str)
        log.info('log_level:'+log_level)

        conn = db_tool.connection_from_db_name(db, save=True)

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
            #调用模块相应函数，获取所有数据
            df = getattr(source_module, get_data_func_name)()
            df['update_date'] = today_str
            df.to_sql(table, conn, index=False, if_exists="replace")
            log.normal("一共获取到{}行数据，已保存到{}表".format(len(df), table))

        log.normal("操作完成。\n")
        conn.close()

        if log_level in ['info', 'debug']: 
            db_tool.db_info(db, table=table, log_level=log_level)
    
    return save_by_once
        
        
def return_function_save_by_start_end(
    data_kind, 
    data_func_name, 
    date_field='trade_date',
):
    """
    闭包，返回函数save_by_start_end
    
    按时间段保存数据: （待优化, 初始值不能设置，在各数据源对应函数默认值。）
    1.查看数据库保存的最后时间
    2.调用数据源对应函数，获最后时间到今天的数据。如：get_futures_date(start_date='2019-01-01', end_date='2020-02-20')
    3.保存到数据库
      
    参数：
    data_kind (str)：数据种类，如'futures'
    data_func_name (str) : 函数名称，如'futures_date'
    date_field (str) : 日期字段名称，默认'trade_date'
    
    示例：
    save_futures_date = return_function_save_by_start_end(data_kind='futures', data_func_name='futures_date')
    save_futures_date为一个函数，执行该函数里的by_start_end函数。
    """    
    @func_time
    def save_by_start_end(source, **keywords):
        #导入与数据源相应模块
        module_name = "dfdata.source.{}.{}".format(source,data_kind)
        source_module = importlib.import_module(module_name)    
        
        #获取数据函数的名称，如：'get_futures_basic'
        get_data_func_name = 'get_{}'.format(data_func_name)  

        my_keywords = KeyWords(keywords, source_kind=source, data_kind=data_kind, data_func_name=data_func_name)
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
            sql = "select {filed_name} from {table_name} order by {filed_name} desc limit 1;".format(filed_name=date_field, table_name=table)
            log.debug("sql: " + sql)
            c = conn.cursor()
            result = c.execute(sql)
            last_dates = result.fetchone()
            last_date_in_table_str = last_dates[0]
            last_date = datetime.datetime.strptime(last_date_in_table_str, my_keywords.config.strftime_format)  
            #print(str('数据库最后时间字符串：' + last_date_in_table_str)+' 格式化字符串：'+str(my_keywords.config.strftime_format) + ' 转化最后时间：' +str(last_date))
            next_date = last_date + datetime.timedelta(days=1)
            next_date_in_table_str = next_date.strftime(my_keywords.config.strftime_format)
            log.normal("数据库最后保存时间：" + last_date_in_table_str)
        except:
            pass

        if next_date_in_table_str <= today_str:
             #调用模块相应函数
            df = getattr(source_module, get_data_func_name)(start_date=next_date_in_table_str, end_date=today_str)
            df.to_sql(table, conn, index=False, if_exists="append")
            log.normal("本次获取到{}行数据，已保存到{}表！".format(len(df), table))
        else:
            log.normal("{}表不需要更新，上次更新时间：{}".format(table, last_date_in_table_str))

        log.normal("操作完成。\n")
        conn.close()

        if log_level in ['info', 'debug']: 
            db_tool.db_info(db, table=table, log_level=log_level)

    return save_by_start_end
    


def return_function_save_by_daily(
    data_kind, 
    data_func_name,
    date_table,
    date_longest_exchange,
    date_field='trade_date',
):
    """
    闭包，返回函数save_by_daily
    
    按天保存数据:  （用于下载日线行情等）
    1.获取所有要下载的交易日集合
    2.获取数据库已有日期集合
    3.上面集合相减，得到要下载日期集合
    4.调用数据源对应函数，获取每天数据，get_{data_func_name}(trade_date)。如：get_futures_daily(trade_date='2020-02-20')
    5.保存到数据库
    
    参数：
    data_kind (str)：数据种类，如'futures'
    data_func_name (str) : 函数名称，如'futures_daily'
    date_table (str) : 时间表，用于从该表获取时间，如'futures_date'，'futures_date'
    date_longest_exchange (str) : 时间表要查询的交易所中时间最长的一个，如save_futures_daily中设置为"CZCE"
    
    示例：
    save_futures_daily
    """ 
    
    @func_time
    def save_by_daily(source, **keywords):
        """   
        按天保存函数

        Parameters:
            # 通用参数
            source (str): 数据源名称
            db (str) : 数据库名称
            table (str) : 数据表名称        

        """   

        #导入与数据源相应数据类别模块
        module_name = "dfdata.source.{}.{}".format(source, data_kind)
        source_module = importlib.import_module(module_name)
        #获取数据函数的名称，如：'get_futures_basic'
        get_data_func_name = 'get_{}'.format(data_func_name)  

        #输入参数和默认参数
        my_keywords = KeyWords(keywords, source_kind=source, data_kind=data_kind, data_func_name=data_func_name)
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
        print(log_level)
       # log.info('log_level:' + log_level)

        #数据库已有
        conn = db_tool.connection_from_db_name(db)
        cur = conn.cursor()
        
        #要下载的交易日集合 all_trade_date_set = set()  
        #先更新日期表 如save_futures_date()
        getattr(this_module, 'save_'+date_table)(source, db=db, log='warning') #log等级设置为warning，普通打印都不会显示
        all_trade_date =  getattr(read_data, 'read_'+date_table)(source, db=db,table=date_table, fields=date_field, exchange=date_longest_exchange, start_date=start_date, end_date=end_date,)
        all_trade_date_set = set(all_trade_date['trade_date'])
        log.normal("一共{}交易日的日行情数据需要下载".format(len(all_trade_date_set)))
        
        
        #数据库已有日期集合
        try:
            #测试不同方法用时
            search_date_direct = False
            start_time = time.perf_counter()
            if search_date_direct == False: #函数查询数据库
                trade_date_in_db = getattr(read_data, 'read_' + table)(source, db=db, table=table, fields=date_field, start_date=start_date, end_date=end_date,)
                trade_date_in_db_set = set(trade_date_in_db['trade_date'])
                log.normal("数据库中已有{}天日行情数据：".format(len(trade_date_in_db_set))) 
            else:  #直接查询
                #还要判断start_date，end_date数据类型，看是否要加引号。
                search_date_sql = "SELECT {} FROM {} WHERE {}>={} and {}<={} ".format(date_field, table, date_field, start_date_sql_format, date_field, end_date_sql_format)
                log.debug("查询日期sql：sql=" + search_date_sql)
                cur.execute(search_date_sql)
                all_date_in_db_result = cur.fetchall()
                trade_date_in_db = []
                for date_tuple in all_date_in_db_result:
                    trade_date_in_db.append(date_tuple[0])
                trade_date_in_db_set = set(trade_date_in_db)
                log.normal("数据库中已有{}天日行情数据：".format(len(trade_date_in_db_set)))         
            end_time = time.perf_counter()
            log.debug("查询数据库已有日期用时：{:.2f}".format(end_time-start_time))    
                      
        except:
            trade_date_in_db_set = set() #如果数据表不存在，就设置已有日期为空集合
            log.normal("数据库中没有日行情数据。")

        #未完成的下载交易日
        trade_date_unfinished = list(all_trade_date_set - trade_date_in_db_set)  
        #下载列表倒序，最近日期比之前日期更常用
        trade_date_unfinished.sort(reverse = True)
        log.normal("未完成下载的交易日数量："+str(len(trade_date_unfinished)))

        for trade_date in trade_date_unfinished: #如果集合中，有要下载的交易日
             #调用模块相应函数，获取所有期货合约
            df = getattr(source_module, 'get_' + table)(trade_date=trade_date)
            log.normal("{} 当天获取到{}行数据。".format(trade_date, str(len(df))))
            df.to_sql(table, conn, index=False, if_exists="append")
            time.sleep(sleep_time) #休息0.5s，因为限制1分钟120次

        conn.close()
        log.normal("数据保存完成。")        

        if log_level in ['info', 'debug']: 
            db_tool.db_info(db, table=table, log_level=log_level)
    
    #返回函数save_by_daily
    return save_by_daily


def return_function_save_by_minute(
    data_kind, 
    data_func_name,
    date_table,
    date_longest_exchange,    
    code_table,
    date_field='trade_date',
    
):
    """
    闭包，返回函数save_by_minute
    
    按天和代码保存数据:  （用于下载分钟数据）
    1.获取所有要下载的交易日集合
    2.获取数据库已有日期集合
    3.上面集合相减，得到要下载日期集合
    4.调用数据源对应函数，获取每天数据，get_{data_func_name}(trade_date)。如：get_futures_daily(trade_date='2020-02-20')
    5.保存到数据库
    
    参数：
    data_kind (str)：数据种类，如'futures'
    data_func_name (str) : 函数名称，如'futures_min'
    date_table (str) : 时间表，用于从该表获取时间，如'futures_date'，'futures_date'
    date_longest_exchange (str) : 时间表要查询的交易所中时间最长的一个，如save_futures_min中设置为"CZCE"
    date_field='trade_date' : 时间字段
    code_table : 标的代码表，用于查找代码的起止时间，如save_futures_min中设置为"futures_basic"
    code_start_field
    code_end_field
    
    示例：
    save_futures_min
    """ 
    
    @func_time
    def save_by_minute(source, **keywords):
        """   
        按分钟保存函数

        Parameters:
            # 通用参数
            source (str): 数据源名称
            db (str) : 数据库名称
            table (str) : 数据表名称
            table (str) : 数据表名称

        """   

        #导入与数据源相应数据类别模块
        module_name = "dfdata.source.{}.{}".format(source, data_kind)
        source_module = importlib.import_module(module_name)
        #获取数据函数的名称，如：'get_futures_basic'
        get_data_func_name = 'get_{}'.format(data_func_name)  

        #输入参数和默认参数
        my_keywords = KeyWords(keywords, source_kind=source, data_kind=data_kind, data_func_name=data_func_name)
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
        code = my_keywords['code']

        if code == None:
            raise Exception("缺少参数：标的代码'code'。")
        
        #数据库已有
        conn = db_tool.connection_from_db_name(db)
        cur = conn.cursor()
        
        #查询code的起止时间，更新start_date和end_date
        code_row = getattr(read_data, 'read_'+code_table)(source, db=db,table=code_table, code=code)
        code_start_date = code_row['start_date'][0]
        code_end_date = code_row['end_date'][0]
        start_date = max(start_date, code_start_date)
        end_date = min(end_date, code_end_date)
        log.info("该标的的起止时间为：code_start_date={}，code_end_date={}".format(code_start_date, code_end_date))
        log.info("下载的起止时间为：start_date={}，end_date={}".format(start_date, end_date))
        
        # 最后一个可能在当天没更新完整，单独更新
        try:
            sql = 'select * from {} where trade_date = (select max(trade_date) and code="{}")'.format(data_func_name, code)
            df_last_date = getattr(read_data, 'read_'+table)(source, db=db, table=table,sql=sql)
            log.normal('数据库中最后一天：' + str(df_last_date))
        except:
            pass
        
        #要下载的交易日集合 all_trade_date_set = set()  
        #先更新日期表 如save_futures_date()
        getattr(this_module, 'save_'+date_table)(source, db=db, log='warning') #log等级设置为warning，普通打印都不会显示
        all_trade_date =  getattr(read_data, 'read_'+date_table)(source, db=db,table=date_table, fields=date_field, exchange=date_longest_exchange, start_date=start_date, end_date=end_date,)
        all_trade_date_set = set(all_trade_date['trade_date'])
        log.normal("一共{}交易日的日行情数据需要下载".format(len(all_trade_date_set)))
        
        
        #数据库已有日期集合
        try:
            #测试不同方法用时
            search_date_direct = False
            start_time = time.perf_counter()
            if search_date_direct == False: #函数查询数据库
                trade_date_in_db = getattr(read_data, 'read_' + table)(source, db=db, table=table, fields=date_field, start_date=start_date, end_date=end_date, code=code)
                trade_date_in_db_set = set(trade_date_in_db['trade_date'])
                log.normal("数据库中已有{}天日行情数据：".format(len(trade_date_in_db_set))) 
            else:  #直接查询
                #还要判断start_date，end_date数据类型，看是否要加引号。
                search_date_sql = "SELECT {} FROM {} WHERE {}>={} and {}<={} and code='{}' ".format(date_field, table, date_field, start_date_sql_format, date_field, end_date_sql_format, code)
                log.debug("查询日期sql：sql=" + search_date_sql)
                cur.execute(search_date_sql)
                all_date_in_db_result = cur.fetchall()
                trade_date_in_db = []
                for date_tuple in all_date_in_db_result:
                    trade_date_in_db.append(date_tuple[0])
                trade_date_in_db_set = set(trade_date_in_db)
                log.normal("数据库中已有{}天日行情数据：".format(len(trade_date_in_db_set)))         
            end_time = time.perf_counter()
            log.debug("查询数据库已有日期用时：{:.2f}".format(end_time-start_time))    
                      
        except:
            trade_date_in_db_set = set() #如果数据表不存在，就设置已有日期为空集合
            log.normal("数据库中没有日行情数据。")

        #未完成的下载交易日
        trade_date_unfinished = list(all_trade_date_set - trade_date_in_db_set)  
        #下载列表倒序，最近日期比之前日期更常用
        trade_date_unfinished.sort(reverse = True)
        log.normal("未完成下载的交易日数量："+str(len(trade_date_unfinished)))

        for trade_date in trade_date_unfinished: #如果集合中，有要下载的交易日
             #调用模块相应函数，获取所有期货合约
            log.debug("开始下载{}当天数据".format(trade_date))
            df = getattr(source_module, 'get_' + table)(trade_date=trade_date, code=code)
            log.normal("{} 当天获取到{}行数据。".format(trade_date, str(len(df))))
            df.to_sql(table, conn, index=False, if_exists="append")
            time.sleep(sleep_time) #休息0.5s，因为限制1分钟120次

        conn.close()
        log.normal("数据保存完成。")        

        if log_level in ['info', 'debug']: 
            db_tool.db_info(db, table=table, log_level=log_level)
    
    #返回函数save_by_minute
    return save_by_minute


#---------------------------------------期货函数----------------------------------------

#保存期货合约表函数
save_futures_basic = return_function_save_by_once(
    data_kind='futures', 
    data_func_name='futures_basic'
)
'''
各数据源获取数据函数：
模块：各数据源的 futures 模块
函数名称：get_futures_basic()
返回值：DataFrame格式，所有期货合约表
返回值要求：合约代码字段为'code'
'''


#保存期货日历表函数
save_futures_date = return_function_save_by_start_end(
    data_kind='futures', 
    data_func_name='futures_date'
)
'''
各数据源获取数据函数：
模块：各数据源的 futures 模块
函数名称：get_futures_date(start_date, end_date)
返回值：DataFrame格式，时间段内期货日历
返回值要求：日期字段为'trade_date'
'''


#保存期货日行情表函数
save_futures_daily = return_function_save_by_daily(
    data_kind='futures', 
    data_func_name='futures_daily',
    date_table='futures_date',
    date_longest_exchange='CZCE',
    date_field='trade_date', 
)
'''
各数据源获取数据函数：
模块：各数据源的 futures 模块
函数名称：get_futures_date(trade_date)
返回值：DataFrame格式，当天期货交易所所有日行情数据
返回值要求：日期字段为'trade_date'，期货代码字段为'code'
'''


#保存期货分钟行情表函数
save_futures_min = return_function_save_by_minute(
    data_kind='futures', 
    data_func_name='futures_min',
    date_table='futures_date',
    date_longest_exchange='CZCE',
    date_field='trade_date', 
    code_table='futures_basic',
    
)
'''
各数据源获取数据函数：
模块：各数据源的 futures 模块
函数名称：get_futures_date(trade_date)
返回值：DataFrame格式，当天期货交易所所有日行情数据
返回值要求：日期字段为'trade_date'，期货代码字段为'code'
'''

#---------------------------------------股票函数----------------------------------------

#保存期货合约表函数
save_stock_basic = return_function_save_by_once(
    data_kind='stock', 
    data_func_name='stock_basic'
)
'''
各数据源获取数据函数：
模块：各数据源的 stock 模块
函数名称：get_stock_basic()
返回值：DataFrame格式，所有期货合约表
返回值要求：合约代码字段为'code'
'''


#保存期货日历表函数
save_stock_date = return_function_save_by_start_end(
    data_kind='stock', 
    data_func_name='stock_date'
)
'''
各数据源获取数据函数：
模块：各数据源的 stock 模块
函数名称：get_stock_date(start_date, end_date)
返回值：DataFrame格式，时间段内期货日历
返回值要求：日期字段为'trade_date'
'''


#保存期货日行情表函数
save_stock_daily = return_function_save_by_daily(
    data_kind='stock', 
    data_func_name='stock_daily',
    date_table='stock_date',
    date_longest_exchange='SSE',
    date_field='trade_date', 
)
'''
各数据源获取数据函数：
模块：各数据源的 stock 模块
函数名称：get_stock_daily(trade_date)
返回值：DataFrame格式，当天期货交易所所有日行情数据
返回值要求：日期字段为'trade_date'，期货代码字段为'code'
'''
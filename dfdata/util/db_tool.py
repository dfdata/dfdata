import os
import sqlite3
import pandas as pd
from dfdata.util.log import Log
from dfdata.util.config import Config, KeyWords
from dfdata.util.func_tool import func_time


################################################################################
### sql语句函数     sql_where_sentence() sql_limit_sentence()
################################################################################

def sql_filter(field_name=None, operator='=', value=None):
    """
    生成单个，sql语句的where的筛选条件字符串,
    
    参数：
    field_name ：字段名（即列名）
    operator ： where语句的操作符，默认=
    **keywods ：关键词字典，输入列名称和值。
    
    示例： 
    sql_filter(field_name='exchange', operator='=',  value='DEC')
    sql_filter('start_date','>=','2020-02-20')
    
    可用操作符：
    =	等于
    <>	不等于
    >	大于
    <	小于
    >=	大于等于
    <=	小于等于
    BETWEEN	在某个范围内
    LIKE	搜索某种模式
    """    
    filter_str = ''
    if field_name not in [None,''] and value not in [None,'']:
        if isinstance (value,(int,float)):   
            #数字值不加单引号'', 其他值加单引号表示字符
            filter_str = '{}{}{} '.format(field_name, operator, value)
        else:
            filter_str = '{}{}\'{}\' '.format(field_name, operator, value)

    return filter_str
    
    

def sql_filters(operator='=', **keywods):
    """
    生成多个sql语句的where的筛选条件字符串, 字段名为字典健名称
    
    参数：
    operator ： where语句的操作符，默认=
    **keywods ：关键词字典，输入列名称和值。
    
    示例： 
    sql_filter(operator='=', code='TC1508.ZCE', exchange='DEC')
    "code='TC1508.ZCE' and exchange='DEC'"
    
    """
    filter_str = ''
    for key,value in keywods.items():
        filter_single_str = sql_filter(key,operator,value)
        if filter_str == '' :
            filter_str = filter_single_str
        elif filter_single_str !='':
            filter_str = filter_str + 'AND ' + filter_single_str
    
    return filter_str 


def sql_filter_start_end_date(field_name='', start_date='', end_date=''):
    """   
    生成sql语句的where部分的start_end部分
    
    如：trade_date >= '2020-02-02' and trade_date <= '2020-02-20'
    
    参数：
    field_name (str) : 日期字段名称，如：trade_date
    start_date ： 开始时间
    end_date : 结束时间
    """ 
    filter_str = ''
    
    if field_name not in ['', None] : 
        start_filter = sql_filter(field_name, '>=', start_date)
        end_filter = sql_filter(field_name, '<=', end_date)
        if start_filter != '' and end_filter != '':
            end_filter = ' AND ' + end_filter 
            
        filter_str = start_filter + end_filter

    return filter_str      
        

def sql_where(*filter_strs):
    """
    生成where部分，
    
    头部加WHERE，将多个filter字符串使用AND连接。
    
    参数：
    """
    where_block = ''  
    need_and = ''
    for filter_str in filter_strs:
        if where_block != '':
            need_and = 'AND '
        if filter_str != '':
            where_block = where_block + need_and + filter_str
    
    if where_block != '':
        where_block = "WHERE " + where_block
        
    return where_block  


def sql_limit(count_and_offset=None):
    """
    生成sql语句的limit部分
    
    参数：
    count_and_offset ：数量(int)或数量和偏移量（元组），
    
    例子:
    sql_limit(5)
    sql_limit((5,3))
    """    
    limit_block=''
    if count_and_offset != None:
        if isinstance (count_and_offset, int):
            limit_block = 'LIMIT {}'.format(count_and_offset)
        elif isinstance (count_and_offset, tuple):  #如：LIMIT 5 OFFSET 2
            limit_block = 'LIMIT {} OFFSET {}'.format(count_and_offset[0], count_and_offset[1])
        else:
            raise Exception("limit参数错误")
    return limit_block

def get_sql(sql=None, fields='*', table=None, where='', limit='',log_level='normal'):
    """
    获取sql语句, 并在logo为info等级以上打印该语句
    
    参数：
    sql：完整sql语句，如果有直接返回该值
    fields：需要选取的列，元组或字符串
    table: 数据表名称
    
    
    例子:
    get_sql(sql=sql, fields=fields, table=table, where=where, limit=limit,log_level=log_level)
    """    
    log = Log(log_level)
    limit_block = sql_limit(limit)  
       
    if sql == '' or sql == None:
        sql = "SELECT {} FROM {} {}{}".format(str(fields), table, where, limit_block)
        log.info('sql="{}"'.format(sql))
    return sql
    


################################################################################
### 
################################################################################

def connection_from_db_name(
    db_name,
    save=False,
    log_level='normal',
):
    """
    根据输入的db_name, 创建数据库连接connection
    -----
    参数：
    db_name 数据库地址名称，如：'data/futures_ts.db'  
    save  默认False，表示用于读取，没有不会新建，True表示没有数据库文件就新建
    log_level  log的等级，
    -----
    返回值：
    sqlite3的数据库连接，Connection
    """
    log = Log(log_level)
        
    #False表示数据库名称用于读取，不会新建数据库
    if save == False:
        try:
            if os.path.isfile(db_name):
                conn = sqlite3.connect(db_name)
                log.info("数据库{}连接成功".format(db_name))
                return conn
        except Exception as e:   
                log.erro('数据库连接出错！')
                raise e
                
    
    # 数据库名称用于保存，不存在就新建
    s = os.path.split(db_name)
    path = s[0]
    db = s[1]
           
    if not os.path.exists(path) and path != '':
            os.makedirs(path)
        
    try:
        conn = sqlite3.connect(db_name)
        log.info("数据库{}连接成功".format(db_name))
    except Exception as e:
        log.error('数据库连接出错！')
        raise e
        
    return conn


def check_file_type(file_name, file_type):
    "判断文件是不是某种类型，是返回True，否则False"
    "已支持的文件类型：sqlite，"
    
    allowable_file_type = ['sqlite', ]
    if file_type not in allowable_file_type:
        raise Exception ("不支持文件类型：{}".format(file_type))
    
    if file_type == 'sqlite': 
        #判断是否为sqlite，sqlite文件头部为：b'SQLite format 3'
        with open(file_name,'rb') as f:
            file_head = f.read(15)
            file_head = file_head.decode()
        if file_head == 'SQLite format 3':
            return True
        else:
            return False
        
    return False
            

    
    
def db_info(
    db=None, 
    table=None,
    log_level='normal',
    info_brief=False,
):
    """   
    数据库信息
    
    输入数据源，默认保存该数据源期货日期表。

    Parameters
    ----------
    db : string
        数据库，，如'tushare', 'jqdata'

    Returns
    -------
    None

    See Also
    --------
    read_trade_cal : 读取期货日期表

    """    
    
    # 输出日志初始化，
    log = Log(log_level)
        
    if db == None:
        download_path = Config.download_path
        listdir = os.listdir(download_path) #获取下载目录里文件列表
        sqlite_files = []  #存储所有sqlite文件的列表
        for file in listdir:
            file_path = download_path + file
            if check_file_type(file_path, 'sqlite'):
                sqlite_files.append(file)
        
        for sqlite_file in sqlite_files:  #递归调用打印所有数据库简介信息
            db_name = download_path + sqlite_file
            db_info(db=db_name, log_level=log_level, info_brief=True)
              
    conn = connection_from_db_name(db)
        
    # 查询数据库文件大小
    db_size_mb = os.path.getsize(db)/1024/1024

    # 查询所有数据库中表
    cur = conn.cursor()
    sql = "select name from sqlite_master where type='table' order by name;"
    all_table = pd.read_sql_query(sql, conn)
    tables = list(all_table.name)
    
    log.normal("数据库{}大小：{:.3f}MB".format(db, db_size_mb))  
    log.normal("数据表共{}张：{}".format(len(all_table),tables))
    
    if table != None :
        tables = [table, ]
        
        
    if info_brief == False: 
    # 查询每个数据表详情
        for table in tables:  
            sql = "select count(*) from '%s'"% table
            r = cur.execute(sql)
            counts = r.fetchone()
            count = counts[0]

            if count > 6:
                sql = "select * from '%s' limit 3"% table
                df_head3 = pd.read_sql_query(sql, conn)
                df_head3.loc['···'] = ["···" for i in range(df_head3.shape[1])] #增加一样省略号
                sql2 = "select * from '%s' limit  %d , 3" % (table, count-3)
                df_last3 = pd.read_sql_query(sql2, conn)
                df_last3.rename(index={0:count-3, 1:count-2,2:count-1}, inplace = True) #修改最后3行的行号
                df_result = df_head3.append(df_last3)
            else:
                sql = "select * from '%s' limit  %d " % (table, count)
                df_result = pd.read_sql_query(sql, conn)

            log.normal("\n数据表{}共有{}行数据。".format(table,count))
            blank_line = ''
            if log_level == 'debug': blank_line = '\n'
            table_line = "-"*80
            table_info_str = "{}{}\n{}\n{}".format(blank_line,table_line,df_result,table_line)
            log.normal(table_info_str)
        
        
    conn.close()

def db_del(
    db,
    table,
    log_level='normal',
):
    # 输出日志初始化，
    log = Log(log_level)
        
    conn = connection_from_db_name(db)
    c = conn.cursor()
    sql = 'drop table {}'.format(table)
    #print('sql = ' + sql)
    try:  
        c.execute(sql)
        conn.close()   #关闭数据库连接
        log.normal('已经删除{}数据库中的{}表格。'.format(db,table))
        db_info(db, info_brief=True)
    except Exception as e:
        print(e)
        conn.close()   #关闭数据库连接
        
        
def db_diff():
    """
    对比两个表每行特定字段的差别，返回不·1同的数据
    -----
    参数：
    table_1 第一个数据库表名称
    table_2 第二个数据库表名称
    fields_1 需要比对的字段，默认为空，比对全部
    fields_2 
    -----
    返回值：
    
    
    -----
    示例：
    db_diff(table_1='f.db/futres_basic')
    
    """
        
        
        
################################################################################
### 数据读取
################################################################################

def return_function_read_data_in_db(data_kind='futures', data_table='futures_date'):
    """
    闭包，返回读取数据库函数
    
    参数：
    data_kind (str)：数据种类，如'futures'
    data_table (str) : 数据表名称，如'futures_date'
    
    示例：
    read_futures_date = return_function_read_data_in_db(data_kind='futures', table='futures_date')
    read_futures_date为一个函数，执行该函数里的read_data_in_db函数。
    """
    
    
    @func_time
    def read_data_in_db(source, **keywords):
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
        my_keywords = KeyWords(keywords, source_kind=source, data_kind=data_kind, table=data_table, function_kind='read')
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
        
        #输入中的参数，没输入赋值None，
        #start_date_input = keywords.get('start_date', None)
       # end_date_input = keywords.get('end_date', None)
        #code_input = keywords.get('code', None)
        #exchange_input = keywords.get('exchange', None)
       # is_open_input = keywords.get('is_open', None)

        

        #打印参数
        log.standard('info', db=db, table=table, today=today_str, log_level=log_level) 

        conn = connection_from_db_name(db)

        if log_level in ['info', 'debug']: 
            db_info(db, table=table, log_level=log_level)

        #日期表生成sql语句
        if data_table in ['futures_date', ]:  
            log.debug("日期表生成sql语句")
            
            if exchange != None:  #如果交易所参数有输入则只显示该列
                fields='trade_date' 
                
            filter_is_open = sql_filter(exchange, '=', is_open)
            filter_start_end_date_str = sql_filter_start_end_date('trade_date', start_date_input, end_date_input)
             
            where = sql_where(filter_start_end_date_str, filter_is_open) 
            try:
                search_sql = get_sql(sql=sql, fields=fields, table=table, where=where, limit=limit, log_level=log_level)
                log.debug("第一次sql：" + search_sql)
                df = pd.read_sql_query(search_sql, conn)
            except:
                where = sql_where(filter_start_end_date_str)
                search_sql = get_sql(sql=sql, fields='*', table=table, where=where , limit=limit, log_level=log_level)
                log.debug("第二次sql：" + search_sql)
                df = pd.read_sql_query(search_sql, conn)                
                
        #其他表生成sql语句
        else:  
            log.debug("其他表生成生成sql语句")
            #生成where语句
            filter_normal = sql_filters(operator='=', code=code, exchange=exchange, trade_date=trade_date)
            filter_start_end_date_str = sql_filter_start_end_date('trade_date', start_date_input, end_date_input)   
            where =sql_where(filter_normal, filter_start_end_date_str)
            
            #生成sql语句，如果有输入sql参数，sql语句就为输入语句。否则按fields，table，where，limit四部分生成。
            search_sql = get_sql(sql=sql, fields=fields, table=table, where=where, limit=limit, log_level=log_level)
            df = pd.read_sql_query(search_sql, conn)

        #关闭连接，返回结果
        conn.close()     
        return df   
    
    #返回函数read_data_in_db
    return read_data_in_db
    
    
import datetime
import time
import pandas as pd
import jqdatasdk as jq
from dfdata.util import config
import dfdata.util.input_parser as input_parser
#从配置文件读取账号密码，登录jqdata

user = config.get_config('jqdata','id')
password = config.get_config('jqdata','password')
jq.auth(user, password)
print('---登录jqdata----')

def save_trade_date_jq(
    db_name='data/futures_jq.db',
    table_name='futures_trade_date', 
):
    """
    保存所有交易日期表 futures_trade_date
    使用jqdata中函数：get_all_trade_days()，get_trade_days()
    网址：https://www.joinquant.com/help/api/help?name=JQData#get_all_trade_days-获取所有交易日
    首先使用get_all_trade_days()下载，以后查询所有交易日期表是最后交易日，然后使用get_trade_days()跟新到今天。
    -----
    参数：
    db_name 设置数据库名称，
    table_name 数据表名称
    -----
    返回值：
    
    
    -----
    示例：
    
    """
    conn = input_parser.Connection_from_db_name(db_name)
    #聚宽数据从2005-01-01开始
    start_date = '2005-01-01'
    #今天日期
    today_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d')

    try:
        #查看数据库最后一天日期
        sql = "select max(trade_date) from {};".format(table_name)
        c = conn.cursor()
        result = c.execute(sql)
        last_date_in_table = result.fetchone()
        start_date=last_date_in_table[0]
    except:
        pass
    
    if start_date != today_date:   #防止重复获取当天日期
        trade_date_array = jq.get_trade_days(start_date=start_date, end_date=today_date)
        df = pd.DataFrame(trade_date_array,columns=['trade_date'])
        df.to_sql(table_name, conn, index=False, if_exists="append")
        print('交易日期表更新完成')
    else:
        print('交易日期表已是最新！')

def get_trade_date_jq(
    db_name='data/futures_jq.db',
    table_name='futures_trade_date', 
    start_date='2005-01-01', 
    count=0,
    end_date='',
    
):
    """
    获取交易日期，
    使用到表futures_trade_date
    首先使用save_trade_date_jq()更新交易日期表，再获取日期，返回列表。
    -----
    参数：
    db_name 设置数据库名称，
    table_name 数据表名称
    -----
    返回值：
    
    
    -----
    示例：
    """   
    conn = input_parser.db_name_save_parser(db_name)
    end_date = input_parser.end_date_parser(end_date, '%Y-%m-%d')
    today_str = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d')
    
    #更新数据库数据
    save_trade_date_jq(db_name=db_name, table_name=table_name)
    
    #数据库中获取数据
    sql = "select trade_date from {} where trade_date >= '{}'and  trade_date <= '{}'".format(table_name,start_date,end_date)
    df = pd.read_sql_query(sql, conn)
    return list(df['trade_date'])
    

def save_futures_basic_jq(
    db_name='data/futures_jq.db',
    table_name='futures_basic', 
):
    """
    保存期货合约表 futures_basic
    使用jqdata中函数：get_all_securities(types=[], date=None)
    网址：https://www.joinquant.com/help/api/help?name=JQData#get_all_securities-获取所有标的信息
    截至2020年3月18日，jqdata中有期货合约数量5579
    首先查询期货合约表是否有当前最近一个交易日数据，没有就重新下载
    -----
    参数：
    db_name 设置数据库名称，
    table_name 数据表名称
    -----
    返回值：

    -----
    示例：
    
    """
    conn = input_parser.db_name_save_parser(db_name)
    #今天时间，如：2020-03-18
    today_str = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d')
    #从聚宽获取最近一个交易日
    last_trade_date_str = jq.get_trade_days(count=1,end_date=today_str)[0].strftime('%Y-%m-%d')
    try:
        #查看数据库，当天有更新就不重新获取，
        sql = "select update_date from {} limit 1;".format(table_name)
        c = conn.cursor()
        result = c.execute(sql)
        update_date_in_table = result.fetchone()
    except:
        pass
    
    if update_date_in_table[0] == last_trade_date_str:
        print("{}表已是最新".format(table_name))
    else:
        futures_codes = jq.get_all_securities(['futures'])
        futures_codes['update_date'] = today_str
        futures_codes = futures_codes.reset_index()
        futures_codes = futures_codes.rename(columns={"index":"code",})
        futures_codes["start_date"] = futures_codes["start_date"].apply(lambda x: x.strftime('%Y-%m-%d'))
        futures_codes["end_date"] = futures_codes["end_date"].apply(lambda x: x.strftime('%Y-%m-%d'))
        futures_codes.to_sql(table_name, conn, index=False, if_exists="replace")
        print("已更新{}表！表中共有{}行数据".format(table_name, len(futures_codes)))
              
    conn.close()
    
    
def get_futures_basic_jq(
    db_name='data/futures_jq.db',
    table_name='futures_basic', 
    code='',
):         
    conn = input_parser.db_name_save_parser(db_name)
    #更新数据库futures_basic表数据
    save_futures_basic_jq(db_name=db_name, table_name=table_name)
    
    sql = "select * from {} where code='{}'".format(table_name,code)
    df = pd.read_sql_query(sql, conn)
    return df
    

def save_futures_daily_jq(    
    db_name='data/futures_jq.db',
    table_name='futures_daily', 
    start_date='2005-01-01', 
    end_date='',
    time_sleep=0.2,
    block_size=3000
):
    """
    保存期货合约表 futures_daily
    使用jqdata中函数：get_price()
    网址：https://www.joinquant.com/help/api/help?name=JQData#get_price-获取行情数据
    截至2020年3月18日，
    首先查询期货合约表，获取所有时间段内所有合约列表，循环获取单个合约
    -----
    参数：
    db_name 设置数据库名称，
    table_name 数据表名称
    time_sleep 获取数据后休息时间，默认0.2秒
    -----
    返回值：
    
    
    -----
    示例：
    
    """
    end_date = input_parser.end_date_parser(end_date, '%Y-%m-%d')
    print("开始下载日期："+start_date)
    print("结束下载日期："+end_date)  
    conn = input_parser.db_name_save_parser(db_name)
    today_str = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d')
    #数据库获取期货合约表表futures_basic
    save_futures_basic_jq(db_name=db_name) #先下载更新期货列表
    futures_codes = pd.read_sql_query("select * from futures_basic;", conn)
    for row in futures_codes.itertuples():
        print('+++++++++start check++++++++')
        code = getattr(row, "code")
        end_date_in_code = getattr(row, "end_date")
        start_date_in_code = getattr(row, "start_date")
        # 获取当前code在futures_daily表中数据最后保存时间（end_date_in_db）
        end_date_in_db = ''
        try:
            c = conn.cursor()
            sql = "select max(trade_date) from futures_daily WHERE code='%s';"%code
            end_date_in_db = c.execute(sql).fetchone()[0]
            end_date_in_db = str(end_date_in_db or '') #如果为None就返回空字符串
        except:
            pass
        print('code: '+code)
        print('end_date_in_code'+end_date_in_code)
        print('end_date_in_db：'+str(end_date_in_db))
        print('start_date：'+str(start_date))
        
        if end_date_in_db != end_date_in_code:  #防止重复获取最后一次数据
            df = jq.get_price(
                code, 
                start_date=max(start_date, end_date_in_db, start_date_in_code),  #从3个日期中取最大值
                end_date=min(end_date, today_str, end_date_in_code), 
                frequency='daily', 
                fields=['open', 'close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit','low_limit', 'avg', 'pre_close', 'paused', 'open_interest'])
            df = df.reset_index()
            df = df.rename(columns={"index":"trade_date",})
            df["trade_date"] = df["trade_date"].apply(lambda x: x.strftime('%Y-%m-%d'))
            df.insert(0, 'code', code)  #最前面插入一列code
            df.to_sql(table_name, conn, index=False, if_exists="append")
            print('有进入！！！')
            time.sleep(time_sleep) #休息时间，默认0.2s
            
        #检测end_date_in_db前未下载数据，对为下载的单个下载
        
        print('-------start end---------')
        
    conn.close()   
        
        
def save_futures_min_jq(    
    db_name='data/futures_jq.db',
    table_name='futures_min', 
    code='',
    start_date='2005-01-01', 
    end_date='',
):
    """
    获取单个合约分钟数据，保存到期货合约表 futures_min
    使用jqdata中函数获取数据：get_price()
    网址：https://www.joinquant.com/help/api/help?name=JQData#get_price-获取行情数据
    截至2020年3月18日，大约
    首先查询期货合约表，获取所有时间段内所有合约列表，循环获取单个合约
    -----
    参数：
    db_name 设置数据库名称，
    table_name 数据表名称
    time_sleep 获取数据后休息时间，默认0.5秒
    code 期货代码
    -----
    返回值：
    
    
    -----
    示例：
    
    """
    end_date = input_parser.end_date_parser(end_date, '%Y-%m-%d')
    print("开始下载日期："+start_date)
    print("结束下载日期："+end_date)  
    conn = input_parser.db_name_save_parser(db_name)
 
    #数据库futures_min表已有日期集合
    try:
        sql = "select trade_date from {} where code='{}';".format(table_name, code)
        df_trade_data = pd.read_sql_query(sql, conn) #获取数据库中trade_date列
        trade_date_in_db = set(df_trade_data['trade_date'].str[0:10]) #数据库中已有日期集合
    except:
        trade_date_in_db = set()  #如果数据表不存在，就设置已有日期为空集合
    print("数据库中已有交易日数量："+str(len(trade_date_in_db)))
    
    #数据库获取合约code的开始时间和结束时间
    df_code = get_futures_basic_jq(db_name=db_name, code=code)
    start_date_code = df_code.start_date[0]
    end_date_code = df_code.end_date[0] 
    #要下载的交易日集合
    start_date=max(start_date, start_date_code)
    end_date=min(end_date, end_date_code)
    trade_date_all = set(get_trade_date_jq(db_name=db_name, start_date=start_date, end_date=end_date))  
    print("要下载交易日数量："+str(len(trade_date_all)))
    
    #未完成的下载交易日
    trade_date_unfinished = trade_date_all - trade_date_in_db      
    print("未完成的下载交易日："+str(len(trade_date_unfinished)))
    unfinished_dates_sorted = list(trade_date_unfinished).sort(reverse=True)
    
    for trade_date in trade_date_unfinished:
        df = jq.get_price(
            code,
            start_date=trade_date,
            end_date=datetime.datetime.strptime(trade_date, "%Y-%m-%d")+datetime.timedelta(days=1),
            frequency='1m', 
            fields=['open', 'close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit','low_limit', 'avg', 'pre_close', 'paused', 'open_interest'])
        print(trade_date+'当天获取到行数：'+str(len(df)))
        df = df.reset_index()
        df = df.rename(columns={"index":"trade_date",})
        df["trade_date"] = df["trade_date"].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        df.insert(0, 'code', code)  #最前面插入一列code
        
        df.to_sql(table_name, conn, index=False, if_exists="append")
        print(trade_date+"当天数据，已保存到数据库！")
        
        time.sleep(0.1) #休息0.5s，因为限制1分钟120次
    
    conn.close()
    print("数据保存完成")


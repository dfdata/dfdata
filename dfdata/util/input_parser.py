import os
import sys
import sqlite3
import datetime

ERROR_MESSAGE = ("可能由于文件夹权限不够或输入错误！\n"
                 "可以尝试如如下设置：\n"
                 "db_name='futures_ts.db'表示当前目录前建立futures_ts.db\n"
                 "db_name='data/futures_ts.db' 表示当前目录的data目录下建立futures_ts.db数据库\n"
                 "db_name='../data/test.db' 表示上级目录下的data目录下建立test.db数据库")


def db_name_save_parser(db_name):
    """
    处理保存数据时用户输入的db_name    
    -----
    输入值：
    数据库地址名称，如：'data/futures_ts.db'   
    -----
    返回值：
    sqlite3的数据库连接，Connection
    """
  
    s = os.path.split(db_name)
    path = s[0]
    db = s[1]
           
    if not os.path.exists(path) and path != '':
        try:
            os.makedirs(path)
        except Exception as e:
            print(e)
            print(error_message)
            sys.exit() 
        
    try:
        conn = sqlite3.connect(db_name)
        print("数据库{}连接成功".format(db_name))
    except Exception as e:
        print(e)
        print('数据库连接出错！')
        sys.exit() 
        
    return conn

def db_name_read_parser(db_name):
    """
    处理读取数据时用户输入的db_name  
    -----
    输入值：
    数据库地址名称，如：'data/futures_ts.db'
    -----
    返回值：
    sqlite3的数据库连接，Connection
    """
    if os.path.isfile(db_name):
        try:
            conn = sqlite3.connect(db_name)
            print("数据库{}连接成功".format(db_name))
            return conn
        except Exception as e:
            print(e)
            print('数据库连接出错！')
            sys.exit() 
    else:
        print(ERROR_MESSAGE)
        sys.exit() 
        
    
def end_date_parser(end_date):
    """
    处理用户输入的tushare终止时间，
    默认返回今天日期，格式如：'20200101'
    """
    if end_date == '':        
        today = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)) #获取现在北京时间，通过utc时间+8小时
        today_str = today.strftime('%Y%m%d') #转化为字符串
        return today_str
    return end_date
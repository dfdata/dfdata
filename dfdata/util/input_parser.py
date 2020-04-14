import os
import sys
import sqlite3
import datetime

ERROR_MESSAGE = ("可能由于文件夹权限不够或输入错误！\n"
                 "可以尝试如如下设置：\n"
                 "db_name='futures_ts.db'表示当前目录前建立futures_ts.db\n"
                 "db_name='data/futures_ts.db' 表示当前目录的data目录下建立futures_ts.db数据库\n"
                 "db_name='../data/test.db' 表示上级目录下的data目录下建立test.db数据库")


def Connection_from_db_name(
    db_name,
    is_in_save=True
):
    """
    处理保存数据时用户输入的db_name    
    -----
    参数：
    db_name 数据库地址名称，如：'data/futures_ts.db'  
    is_in_save 默认True，表示数据库名称用于保存，False表示数据库名称用于读取
    -----
    返回值：
    sqlite3的数据库连接，Connection
    """
    
    #False表示数据库名称用于读取
    if is_in_save == False:
        try:
            if os.path.isfile(db_name):
                conn = sqlite3.connect(db_name)
                print("数据库{}连接成功".format(db_name))
                return conn
        except Exception as e:   
                print(e)
                print('数据库连接出错！')
                sys.exit()     
    
    # 数据库名称用于保存
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


def check_table_name(table_name):

    
    return table_name
    
            
def check_end_date(end_date, str_tpye='%Y%m%d'):
    """
    处理用户输入的终止时间，
    默认返回今天日期，格式如：'20200101'
    -----
    输入值：
    end_date 输入要处理的日期字符串
    tpye 字符串格式化类型，默认'%Y%m%d'
    -----
    返回值：
    字符串
    """
    
    
    if end_date == '':        
        today = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)) #获取现在北京时间，通过utc时间+8小时
        today_str = today.strftime(str_tpye) #转化为字符串
        return today_str
    return end_date
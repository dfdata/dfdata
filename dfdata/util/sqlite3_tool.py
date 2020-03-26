import os
import sqlite3
import pandas as pd
import dfdata.util.input_parser as input_parser

def db_info(db_name):
    conn = input_parser.db_name_read_parser(db_name)
    # 查询数据库文件大小
    db_size_mb = os.path.getsize(db_name)/1024/1024
    print("数据库{}简介信息如下：".format(db_name))
    print("数据库大小：{:.3f}MB".format(db_size_mb))
    # 查询所有数据库中表
    cur = conn.cursor()
    sql = "select name from sqlite_master where type='table' order by name;"
    all_table = pd.read_sql_query(sql, conn)
    tables = list(all_table.name)
    print("一共{}张数据表：{}".format(len(all_table),tables))
    
    # 查询每个数据表详情
    for table in tables:  
        sql = "select count(*) from '%s'"% table
        r = cur.execute(sql)
        count = r.fetchone()
        print("")
        print("数据表{}共有{}行数据。".format(table,count[0]))
        sql = "select * from '%s' limit 5"% table
        df_head5 = pd.read_sql_query(sql, conn)
        print(df_head5)
    conn.close()

def db_drop_tabel(db_name,table_name):
    conn = input_parser.db_name_read_parser(db_name)
    c = conn.cursor()
    sql = 'drop table {}'.format(table_name)
    #print('sql = ' + sql)
    try:  
        c.execute(sql)
        print('已经删除{}数据库中的{}表格。'.format(db_name,table_name))
        conn.close()   #关闭数据库连接
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
        
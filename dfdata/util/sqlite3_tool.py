import os
import sqlite3
import dfdata.util.input_parser as input_parser

def db_info(db_name):
    conn = input_parser.db_name_read_parser(db_name)
    # 查询数据库文件大小
    db_size_mb = os.path.getsize(db_name)/1024/1024
    print("数据库{}大小为：{:.3f}MB".format(db_name,db_size_mb))
    # 查询所有数据库中表
    cur = conn.cursor()
    sql = "select name from sqlite_master where type='table' order by name;"
    cur.execute(sql)
    all_table = cur.fetchall()
    print("数据库{}中所有数据表：{}".format(db_name,all_table))
    # 查询每个数据表详情
    for table in all_table:  
        sql = "select count(*) from '%s'"% table
        r = cur.execute(sql)
        count = r.fetchall()
        print("数据表{}共有{}行数据。".format(table,count))
        
    conn.close()

def drop_tabel(db_name,table_name):
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
import jqdatasdk as jq
from dfdata.util import config
#从配置文件读取账号密码，登录jqdata

user = 
password = 
jq.auth(user, password)

def save_jq_futures_daily(    
    db_name='data/futures_jq.db',
    table_name='futures_daily_jq', 
    start_date='20050101', 
    end_date=''
    sub_count=3000
):
    """
    
    """
    end_date = input_parser.end_date_parser(end_date)
    print("开始下载日期："+start_date)
    print("结束下载日期："+end_date)  
    conn = input_parser.db_name_save_parser(db_name)

    futures_codes = get_all_securities(['futures'])  #所与期货列表
    if start_date <= end_date:
    df = jq.get_price(futures_codes, start_date=start_date, end_date=None, frequency='daily', fields=None, skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
        
        
def save_jq_futures_min(    
    db_name='data/futures_jq.db',
    table_name='futures_min_jq', 
    start_date='20050101', 
    end_date=''
    sub_count=3000
):
    """
    
    """
    end_date = input_parser.end_date_parser(end_date)
    print("开始下载日期："+start_date)
    print("结束下载日期："+end_date)  
    conn = input_parser.db_name_save_parser(db_name)

    futures_codes = get_all_securities(['futures'])  #所与期货列表
    if start_date <= end_date:

get_price(security, start_date=None, end_date=None, frequency='daily', fields=None, skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)

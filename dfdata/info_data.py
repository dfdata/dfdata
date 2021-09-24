from dfdata.util.log import Log
from dfdata.util.config import KeyWords
from dfdata.util import db_tool
from dfdata.util.func_tool import func_time



def return_function_info_data(data_kind, data_func_name):
    """
    闭包，返回读取数据库函数
    
    参数：
    data_kind (str)：数据种类，如'futures'
    data_func_name (str) : 数据表名称，如'futures_date'
    
    示例：
    info_futures_basic = return_function_info_data(data_kind='futures', data_func_name='futures_date')
    info_futures_basic为一个函数，执行该函数里的info_data函数。
    """
    
    
    @func_time
    def info_data(source, **keywords):
        """   
        查看配置文件夹中的数据库文件

        Parameters:
            source (str): 数据源名称
            db (str) : 数据库名称
            log (str) : log等级，如info, debug等，默认normal,


        示例：
        info_db()    查看下载文件夹下所有数据库


        """   
        #输入参数和默认参数
        my_keywords = KeyWords(keywords, source_kind=source, data_kind=data_kind, data_func_name=data_func_name, function_kind='read')
        db =  my_keywords["db"]
        data_table =  my_keywords["table"]
        log_level = my_keywords['log']
        log = Log(log_level) #初始化log等级

        #打印参数
        log.standard('normal', db=db, table=data_table)   
        log.info('log_level='+log_level)
        db_tool.db_info(db=db, table=data_table, log_level=log_level)
    
    #返回函数info_data
    return info_data


    
    
################################################################################
### 期货函数  futures
################################################################################

#函数，本地读取期货日期表   
info_futures_date = return_function_info_data(data_kind='futures', data_func_name='futures_date')

#读取期货合约表函数
info_futures_basic = return_function_info_data(data_kind='futures', data_func_name='futures_basic')

#读取期货日线表函数  futures_daily
info_futures_daily = return_function_info_data(data_kind='futures', data_func_name='futures_daily')

#读取期货日线表函数  futures_daily
info_futures_min = return_function_info_data(data_kind='futures', data_func_name='futures_min')



################################################################################
### 股票函数  stock
################################################################################

info_stock_date = return_function_info_data(data_kind='stock', data_func_name='stock_date')

info_stock_basic =  return_function_info_data(data_kind='stock', data_func_name='stock_basic')

info_stock_daily = return_function_info_data(data_kind='stock', data_func_name='stock_daily')
    
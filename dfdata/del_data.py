from dfdata.util.log import Log
from dfdata.util.config import KeyWords
from dfdata.util import db_tool
from dfdata.util.func_tool import func_time


@func_time
def del_table(source, table, **keywords):
    """   
    从数据库读取数据

    Parameters:
        source (str): 数据源名称
        db (str) : 数据库名称
        table (str) : 数据表名称
        log (str) : log等级，如info, debug等，默认normal,

    """   
    data_kind = table.split('_')[0]
    #输入参数和默认参数
    my_keywords = KeyWords(keywords, source_kind=source, data_kind=data_kind, data_func_name=table, function_kind='read')
    db =  my_keywords["db"]
    data_table =  my_keywords["table"]
    log_level = my_keywords['log']
    log = Log(log_level) #初始化log等级

    #打印参数
    log.standard('normal', db=db, table=data_table)   
    log.info('log_level='+log_level)
    db_tool.db_del(db=db, table=table, log_level=log_level)

    

        
        
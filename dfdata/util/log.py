import sys
import time
from dfdata.util.config import Config


"""
输出显示等级：
debug :  调试时候出输出信息
info :  详细输出信息
normal :  正常输出信息
warning : 警告时候输出信息
error :   错误时候输出信息

默认等级为normal，不会输出info和debug内容
当设置为info时候，会输出除debug的内容
当设置为debug，会输出所有内容

使用：
#导入
from dfdata.util.log import Log

#输出info信息：
log = Log() #指定设置中的log等级
log = Log("info") #指定info等级的log

log.info() 
"""

class Log():
    
    def __init__(self, level=None):
        self.level = self.get_level(level)
          
    #获取设置中level等级
    def get_level(self, level):
        if level == None:
            level = Config.log_level
            return level
        else:
            return level

    #获取输出头部信息
    def get_head_str (self, level):
        'log等级为debug，返回头部信息，包含执行位置的时间，文件名，函数名'
        if level == 'debug':           
            # 获得当前时间
            time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) 
            # 调用者文件名
            file_name = sys._getframe().f_back.f_back.f_code.co_filename                        
            # 调用者函数名                   
            func_name = sys._getframe().f_back.f_back.f_code.co_name
            head_str = time_now+' '+file_name+' '+func_name+' : '
            return head_str
        else:
            return ''
        
        
    
    def debug(self, message,):
        """
        debug函数：调试时候出输出信息
        
        在log等级为'debug'中显示
        """
        level = self.level
        
        if level in ['debug']:
            head_str = self.get_head_str(level)
            print(head_str + str(message))

            
    def info(self, message, ):
        """
        info函数：详细输出信息
        
        在log等级为'info', 'debug'中显示
        """        
        level = self.level
        
        if level in ['info', 'debug']:
            head_str = self.get_head_str(level)
            print(head_str + str(message))

            
    def normal(self, message,):
        """
        normal函数：普通输出信息
        
        在log等级为'normal', 'info', 'debug'中显示
        """   
        level = self.level
        
        if level in ['normal', 'info', 'debug']:
            head_str = self.get_head_str(level)
            print(head_str + str(message))    

            
    def warning(self, message, ):
        """
        warning函数：警告时候输出信息
        
        任何时候都输出
        """
        level = self.level
        head_str = self.get_head_str(level)
        
        prefix = '提醒：'
        message = '\033[1;30;43m' + head_str + prefix + str(message) + '\033[0m' #设置字体为黄色高亮
        print(message)    

        
    def error(self, message,):
        """
        error等级：错误时候输出信息
        
        任何时候都输出
        """        
        level = self.level
        head_str = self.get_head_str(level)
        
        prefix = '错误：'
        message = '\033[1;30;41m' + head_str + prefix + str(message) + '\033[0m'  #设置字体为红色高亮
        print(message)    
        
    
    # 标准格式化输出，
    #如 standard('info',db="test.db") 调用info()函数，打印：数据库名称：db='test.db'
    def standard(self, log_show_level='normal', **keywords):
        log_function =  getattr(Log, log_show_level)  #根据log等级字符串调用相应的方法，默认Log.normal函数
        for key, value in keywords.items():
            if key == 'db':
                result = "数据库名称：db='{}'".format(value)
            if key == 'table':
                result = "数据表名称：table='{}'".format(value)
            if key == 'today' or key == 'today_str':
                result = "今天日期：{}".format(value)
            if key == 'log' or key == 'log_level' :
                result = "当前log等级：log={}".format(value)
            if key == 'start_date' :
                result = "开始时间：start_date={}".format(value)
            if key == 'end_date' :
                result = "结束时间：end_date={}".format(value)
                
            log_function(self, result)

    

        

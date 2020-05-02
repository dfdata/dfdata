import time
from functools import wraps
from dfdata.util.log import Log


def func_time(func):
    @wraps(func)
    def count_time(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs) #调用执行原函数
        end_time = time.time()

        try:
            log_level = kwargs['log'] #如果有传入log等级参数
            log = Log(log_level)  #初始化log
        except:
            log = Log()  #log初始化
        
        log.debug("{}模块的{}函数的可变参数*args：{}".format(func.__module__, func.__name__, str(args)) )
        log.debug("{}模块的{}函数的关键字参数**kwargs：{}".format(func.__module__, func.__name__, str(kwargs)) )
        log.info("{}模块的{}函数用时：{:.4f}秒".format(func.__module__, func.__name__, (end_time-start_time)) )
        return result      #返回原函数返回值
    return count_time
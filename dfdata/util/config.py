#配置文件
import datetime
import configparser
import os
import importlib
import pkgutil   
import dfdata.source
from dfdata import default_config


#所有数据源包下包的名称
all_sources = []
for module_info in pkgutil.iter_modules(dfdata.source.__path__):
    all_sources.append(module_info.name)

allowable_config_sections = all_sources + ['main', ]
allowable_config_keys = default_config.allowable_config_keys
allowable_arg_names = default_config.allowable_arg_names



# -----------------------------------------------------------------------------
# 配置函数 get_file_config  set_config  reset_config  get_config   
# -----------------------------------------------------------------------------

""" 
配置存放位置和顺序：
1.用户配置文件中，各数据源（source）的配置
2.用户配置文件中，通用配置（main）的设置
3.各数据源的default_config文件
4.主程序的default_config文件


用户配置文件可设置值，示例如下：
[main]     # 主配置，所有数据源通用。
download_path = ~/dfdata/   #保存目录，默认用户目录下的dfdata目录
log = normal                #配置输出信息等级，默认等级normal 
start_date = 2010-01-01     #保存save类函数开始时间
sleep_time = 0.5            #函数内有time.sleep()的参数值。

[tushare]   # 各数据源（source）的配置，会覆盖主配置的值
start_date = 2005-01-01
sleep_time = 0.5

""" 


# 读取用户配置文件，没有就返回None
def get_file_config(section=None, key=None):
    # 使用expanduser展开成完整地址
    config_file_path = os.path.expanduser(default_config.config_file) 
    config = configparser.ConfigParser()
    config.read(config_file_path)    #读取配置文件
      
    #如果key为空，打印配置文件section下键和值，
    #如果section也为空，打印所有section下键和值
    if key==None :
        all_sections = [section, ]
        if section == None:
            all_sections = config.sections()
            if 'main' in all_sections: #将'main'显示在最前面
                all_sections.remove('main')
                all_sections.insert(0, 'main')
        for section in all_sections:
            print('[{}]'.format(section))
            #打印每个section的所有键值对
            for key,value in config.items(section):
                print(key,'=',value)  
            print()
        return None
 
    try:
        value = config[section][key]     #获取对应的值
    except:
        value = None       
        
    return value


# 设置用户配置文件
def set_config(section='main', **kwargs):
    # 检查section是否合法
    if section not in allowable_config_sections:
        raise Exception("section名称不正确："+section)
    
    config_file = default_config.config_file
    comfig_file_expand = os.path.expanduser(config_file)
       
    config = configparser.ConfigParser()
    config.read(comfig_file_expand)

    if section not in config:
        config.add_section(section)  #添加section

    for k,v in kwargs.items():    
        if k not in allowable_config_keys:
            raise Exception("键名称不正确："+k)
        if v == None: # 如果值为None，删除该键值对。等于重置为默认值
            config.remove_option(section, k)
            if len(config.options(section)) == 0: #如果section下没有键值对，
                config.remove_section(section)   #删除该section
            continue
        if k == 'download_path':  #如果如下载路径，检查目录并创建
            v = format_path_str(v, mkdir=True)
        config.set(section, k, v)

    with open(comfig_file_expand, 'w') as configfile:
        config.write(configfile) 
    
    print('配置写入成功。')

    
# 重置为默认配置，即删除用户配置文件
def reset_config(): 
    config_file = default_config.config_file
    config_file_expand = os.path.expanduser(config_file)
    
    if(os.path.exists(config_file_expand)):
        os.remove(config_file_expand)
        print("已删除配置文件: {}，已重置为默认配置。".format(config_file_expand))
    else:
        print("配置文件不存在，为默认配置。")

    
    
    
# 获取配置，没有返回None
# 最终参数使用各数据源做section参数，如get_config('tushare', 'start_date')
def get_config(section=None, key=None):    
    """
    
    示例：
    get_config(): 获取所有配置
    get_config('main'): 获取main所有配置
    get_config('tushare'): 获取tushare所有配置
    get_config('tushare','start_date'): 获取tushare下载开始时间
    get_config('main','start_date'): 获取通用配置下载开始时间
    get_config('main', 'download_path'): 获取下载路径
    """
    #从文件中获取值，没有就为None
    value = get_file_config(section,key)
    
    if key == None:  #打印所有配置信息，返回None
        sections = [section, ]
        if section == None:
            sections = allowable_config_sections #如果有section有值，就只打印该section下的值
            
        for allowable_section in sections:
            section_result = {} 
            for allowable_key in allowable_config_keys:
                value = get_config(allowable_section, allowable_key)
                if value != None:
                    section_result[allowable_key] = value
            #打印输出section内容
            if section_result:  #不为空
                print('[{}]'.format(allowable_section))
                for k, v in section_result.items():
                    print('{} = {}'.format(k,v))
                print('') 
        return None  #打印所有配置信息后，返回None          

    if section == 'main':  #通用配置 main
        if value == None:
            value = getattr(default_config, key, None)
        
    else:  #各资源类配置
        if value == None:
            value = get_file_config('main',key)  #查看main下是否有配置
            #print("用户配置文件该资源无该配置值", '获取main.',key,'=',value)
            if value == None:
                module_source_config = importlib.import_module('dfdata.source.{}.default_config'.format(section))
                value = getattr(module_source_config, key, None)
                #print('获取资源default_config.',key,'=',value)
      
    #print(section,".", key," = ", value)
    #格式化地址
    if key == 'download_path' and value != None:
        value = format_path_str(value)
        
    #格式化时间
    if key == 'start_date' and value != None:
        value = format_time_str(value, '%Y-%m-%d')
    
    #print('{}:{}'.format(key,value))
    return value


# -----------------------------------------------------------------------------
# 输入格式化函数  format_time_str 
# -----------------------------------------------------------------------------

def format_time_str(_input, strftime_format):
    """   
    格式化输入时间，返回某种格式字符串，

    format_time_str('2020-02-20', '%Y%m%d') 返回：'20200220'
    """         
    if isinstance(_input,int): #如果为数字，转为字符串，再进一步转化
        _input = str(_input)

    if isinstance(_input,str): #如果为字符串格式，转为时间       
        _input = _input.replace("-","")
        _input = _input.replace(".","")
        _input = datetime.datetime.strptime(_input, '%Y%m%d') #转为时间格式

    date_str = _input.strftime(strftime_format) 
    return date_str


def format_path_str(path, mkdir=False):
    """   
    格式化输入文件目录，返回末尾带斜杠'/'的目录地址字符串，如'~/data/'
    
    mkdir 是否立即创建该目录，默认不创建
    
    支持的目录地址如下：
    '~/data'  用户目录下的data目录，不随程序变动
    /data    根目录下的data目录， 不随程序变动
    'dfdata'    当前程序运行的目录下的dfdata目录，随程序变动
    ''        当前程序运行的目录下，随程序变动
    format_path_str('2020-02-20', '%Y%m%d') 返回：'20200220'
    """    
    path = str(path)
    if path != '': #为空不用加斜杠/
        if path[-1] != '/':
            path = path + '/'
    
    if mkdir != True: #创建目录
        if not os.path.exists(path) and path != '':
            os.makedirs(path)        
    
    return path

        
        
# -----------------------------------------------------------------------------
# 配置类 Config
# -----------------------------------------------------------------------------

class Config:
   
    download_path = get_config('main','download_path')  #获取下载位置配置，默认用户目录下：'~/dfdata/'
    log_level = get_config('main','log')     #获取打印信息日志等级，默认正常等级，'normal'
    log = log_level
    allowable_arg_names = allowable_arg_names   #允许函数输入的参数名称，不在这列表中报参数错误。
    source_names = all_sources   #所有数据源名称列表，如['tushare','collect']

   
    def __init__(self, source_kind):
        
        #初始化时，判断输入数据源名称是否合法，
        if source_kind not in Config.source_names:
            raise ValueError("数据源名称错误!") 
           
        module_source_config = importlib.import_module('dfdata.source.{}.default_config'.format(source_kind))
        
        self.name = source_kind+" config"
        self.kind = source_kind
        self.source_config = module_source_config
        self.main_config = default_config
        self.download_path = self._get_download_path()    #数据源的默认数据库地址名称
        self.log = get_config('main','log')
        self.postfix = self.source_config.postfix        
        self.strftime_format = self.source_config.strftime_format  #数据源的时间转字符串格式
        self.today_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))  #今天日期
        self.today =  self.today_time.strftime(self.strftime_format)  #今天日期字符串，按数据源对应格式
        self.yesterday = (self.today_time - datetime.timedelta(days=1)).strftime(self.strftime_format) #昨天日期字符串，按数据源对应格式
        self.start_date = self._get_start_date()  #获取设置开始时间字符串, 按数据源格式
        self.end_date_time = self.today_time
        self.end_date = self.today
        self.sleep_time = default_config.sleep_time
        
    # 获取数据库名称配置
    def _get_download_path(self):
        download_path = get_config('main','download_path') 
        download_path = os.path.expanduser(download_path)

        return download_path        
    
        
    # 获取下载的开始时间
    # 取main和source中最大值
    def _get_start_date(self):
        start_date = get_config(self.kind,'start_date')
        start_date = format_time_str(start_date, self.strftime_format)  #格式化字时间
        return start_date

    

    
  
# -----------------------------------------------------------------------------
# 参数字典类 KeyWords
# -----------------------------------------------------------------------------

class KeyWords(dict):
    """
    参数字典类，继承于字典类

    参数获取顺序：
    1. 用户在函数中输入
    2. __missing__函数定义的默认值
    
    
    __missing__函数设置顺序：
    1. Config中的source_config里的函数的参数（如果有）
    2. Config类中参数
    
    """  
        
    def __init__(self,input_dict={}, source_kind=None, data_kind=None, data_func_name=None, function_kind='save'):
        """
        初始化
        input_dict (dict) : 用户输入的参数
        source_kind (str) ：数据源类别
        data_kind (str) ：数据类别，如'futures', 'stock'
        table (str) : 表名称
        function_kind (str) : 函数类别，默认'save'，参数缺失时使用默认填充，'read',有些参数不使用默认值如start_date 
        """
        KeyWords.source_kind=source_kind
        KeyWords.table=data_func_name
        KeyWords.data_kind=data_kind
        KeyWords.config = Config(source_kind)
        KeyWords.function_kind = function_kind
        KeyWords.start_date = self._get_func_start_date()
        KeyWords.end_date = self._get_func_end_date()
            
        for k,v in input_dict.items():      
            #处理输入参数字典, 按键和数据源类型，返回对应格式的值
            v = self._input_parser(k,v) 
            
            #初始化参数字典
            if isinstance(v,dict):
                self.__setitem__(k,KeyWords(v,KeyWords.source_kind, KeyWords.data_kind, KeyWords.table, KeyWords.function_kind))
            else:
                self.__setitem__(k,v)
                
        #在debug模式中打印参数信息
        from dfdata.util.log import Log
        try:
            log_level = input_dict['log']
        except:
            log_level = 'normal'
        log = Log(log_level) #初始化log等级
        log.debug('输入参数初始化信息：') 
        log.debug('输入参数字典：input_dict = ' + str(input_dict))       
        log.debug('数据源：source_kind = ' + str(source_kind)) 
        log.debug('数据类别：data_kind = ' + str(data_kind)) 
        log.debug('表名称：table = ' + str(KeyWords.table))  
        
     
  
    #初始化参数字典
    def __setitem__(self,k,v):
        dict.__setitem__(self,k,v)
        dict.__setattr__(self,k,v)
        
        
    #处理输入参数字典
    def _input_parser(self, k, v):   
        
        # 检测参数名称是否合法"
        if k not in KeyWords.config.allowable_arg_names:
            raise Exception('输入参数名称错误: {}'.format(k))
        
        #按键和数据源类型，返回对应格式的值"
        date_key_list = ['start_date', 'end_date', 'trade_date']
        if k in date_key_list:
            v= format_time_str(v, KeyWords.config.strftime_format)  
        return v
                
    
        
    # 未输入参数，
    # save类函数缺失参数的处理，设置为Config的默认参数
    # read类函数,有些参数不使用默认值如start_date, end_date
    # 未设置返回None
    def __missing__(self,k): 
        # save类read类函数，返回相同的值
        if k == "db" :  
            db_name =KeyWords.config.download_path + KeyWords.data_kind + KeyWords.config.postfix + '.db'
            self.__setitem__(k,db_name)
            return db_name
        if k == "table" :
            table_name = KeyWords.table
            self.__setitem__(k,table_name)
            return table_name
        if k == 'sql': #sql语句，默认为None
            sql = None
            self.__setitem__(k,sql)
            return sql        
        if k == 'fields': #sql语句中获取的字段，默认查询全部字段
            fields = '*'
            self.__setitem__(k,fields)
            return fields  
        if k == 'is_open': #是否开市，默认1，表示开市
            is_open = 1
            self.__setitem__(k,is_open)
            return is_open  
        
        key_list = ['today','today_str',
               'log',  'sleep_time']
        if k in key_list:
            value = getattr( KeyWords.config, k)
            self.__setitem__(k, value)
            return value
        
        # save类read类函数，返回不同的值
        key_list_for_different_functions = ['start_date','end_date',]
        if k in key_list_for_different_functions:
            
            # save类函数中, 缺失值设置为Config中的值
            if KeyWords.function_kind == 'save': 
                value = getattr(KeyWords, k)
                self.__setitem__(k, value)
                return value
            
            # read类函数中， 缺失值设置为None
            if KeyWords.function_kind == 'read': 
                return None
        
        return None
    
    
    # 获取函数默认配置：
    def _get_func_default_config(self, key):
        '''
        获取函数默认参数
        
        位置：主default_config和数据源的default_config
        
        顺序：
        1.数据源默认配置的函数表名参数
        2.数据源默认配置的参数
        3.主默认配置的函数表名参数
        4.主默认配置的参数
        '''
        value = getattr(KeyWords.config.source_config, KeyWords.table,{key:None})[key]
        if value == None:
            value = getattr(KeyWords.config.source_config, key, None)
            if value == None:
                value = getattr(KeyWords.config.main_config, KeyWords.table,{key:None})[key]   
                if value == None:
                    value = getattr(KeyWords.config.main_config, key, None)
                   
        return value
   
    def _get_func_start_date(self):
        start_date_in_config = KeyWords.config.start_date
        start_date_in_default_config = self._get_func_default_config(key='start_date')
        start_date_in_default_config = format_time_str(start_date_in_default_config, KeyWords.config.strftime_format) #格式化配置中时间字符串

        
        start_date = max(start_date_in_default_config, start_date_in_config)   
        
        return start_date
            
    def _get_func_end_date(self):  
        #今天3点前返回前一天的函数列表
        before_330pm_last_days = ['futures_daily', ]
        if KeyWords.table in before_330pm_last_days:
            now_time =  KeyWords.config.today_time
            #print("现在时间："+str(now_time))
            if now_time.time() < datetime.time(15, 30, 1, 123456):
                end_date = KeyWords.config.yesterday
                return end_date
        
        #其他返回 京时间，今天
        return KeyWords.config.end_date   
        
    
    __setattr__=__setitem__
    __getattr__=__missing__     
    
    

    

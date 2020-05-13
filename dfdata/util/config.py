#配置文件
import datetime
import configparser
import os

""" 
配置存放位置：配置文件和defalut_config字典
获取顺序：1.配置文件 2.defalut_config字典

配置值获取顺序数：1.各数据源（source）的设置 2.主要配置（main）的设置

配置获取顺序：
1.配置文件各source下配置
2.defalut_config字典各source下配置
3.配置文件主要配置（main）的设置
4.defalut_config字典主要配置（main）的设置


配置文件可设置值：
[main]     # 主要配置，所有数据源通用。
download_path = ~/dfdata/   #保存目录，默认用户目录下的dfdata目录
log = normal                #配置输出信息等级，默认等级normal 
start_date = 2010-01-01     #保存save类函数开始时间
sleep_time = 0.5            #函数内有time.sleep()的参数值。

[tushare]   # 各数据源配置，会覆盖主要配置的值
start_date = 2005-01-01
sleep_time = 0.5


""" 

# 数据源collect配置
collect_config = {  
    'postfix':'_ct',  #后缀，用于数据库名称
    'strftime_format':'%Y-%m-%d', # 日期转时间格式
}  

# 数据源tushare配置  
tushare_config = { 
    'postfix':'_ts',  #后缀，用于数据库名称
    'strftime_format':'%Y%m%d',
    'start_date' : '19900101',
    'futures':{ #期货设置
        'exchange' : {  #期货交易所代码和名称字典
            'CZCE':'郑州商品交易所',
            'SHFE':'上海期货交易所',
            'DCE':'大连商品交易所',
            'CFFEX':'中国金融期货交易所',
            'INE':'上海国际能源交易所'
        },
        'futures_daily':{
            'start_date' : '19960101',
        },  
        
    },
     'stock':{ #股票设置
     },

}

# 数据源jqdata配置
jqdata_config = {  
    'postfix':'_jq',  #后缀，用于数据库名称
    'strftime_format':'%Y-%m-%d',
    'start_date' : '20050101',
    'id' : '', #用户账号
    'password' : '',  #用户密码   
    'futures':{ #期货设置
        'exchange' : {  #期货交易所代码和名称字典
            'XZCE':'郑州商品交易所',
            'XSGE':'上海期货交易所',
            'XDCE':'大连商品交易所',
            'CCFX':'中国金融期货交易所',
        },      
       
    },
     'stock':{ #股票设置
     },
    
}


    
# 默认配置
defalut_config = {  
    
    #主要配置
    'main':{  
        'download_path' : '~/dfdata/',  #下载位置，默认在用户目录下的dfdata目录
        'config_file' : "~/configs/dfdata.ini",    #配置文件，默认在用户目录configs/dfdata.ini
        'log': 'normal',   #配置输出信息等级，默认等级normal
        'start_date' : '1900-01-01',  #开始时间
        'sleep_time' : 0.5 , 


    },
    
    # 限制输入的参数名称等
    # 防止用户输错
    'allowable':{
        'allowable_config_sections' : [ #可用配置文件section名称列表
            'main',
            #数据源名称
            'collect','tushare','jqdata',
        ],
        
        'allowable_config_keys' : [  #可用配置文件键值对的键名称列表。
            'download_path', 'config_file', 'log', 'start_date','sleep_time',
            'id', 'password',
        ],
        
        'allowable_arg_names' : [  #允许的参数名称, 如果没出现在该列表，会抛出参数错误异常
                'source', 'db', 'table','start_date','end_date','sleep_time',
                'fields','sql', 'limit',    #sql查询参数-通用
                'exchange', 'code',  'trade_date',       #sql查询参数-字段
                'log',
                'is_open',     #tushare中
                ],        
        
    },
    
   
    # 数据配置，
    # 1.用于设置数据库名称
    'data':{
        'futures':{},
        'stock':{},
    },
    
    # 数据源配置
    'source':{
        'collect' : collect_config,
        'tushare' : tushare_config,
        'jqdata' : jqdata_config,       
    },

    
}

allowable_config_sections = defalut_config['allowable']['allowable_config_sections']
allowable_config_keys = defalut_config['allowable']['allowable_config_keys']
allowable_arg_names = defalut_config['allowable']['allowable_arg_names']

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
# 配置函数
# -----------------------------------------------------------------------------

# 从配置文件读取配置，没有就返回None
def _get_file_config(section, key):
    # 使用expanduser展开成完整地址
    config_file_path = os.path.expanduser(defalut_config['main']['config_file']) 
    config = configparser.ConfigParser()
    config.read(config_file_path)    #读取配置文件

    try:
        value = config[section][key]     #获取对应的值
    except:
        value = None       
        
    return value
    

# 获取配置
# 没有返回None
def get_config(section=None, key=None):    
    """
    
    示例：
    get_config(): 获取所有配置
    get_config('tushare'): 获取tushare所有配置
    get_config('main'): 获取main所有配置
    get_config('main', 'download_path'): 获取下载路径
    get_config('main','start_date'): 获取下载开始时间
    """
    #从文件中获取值，没有就为None
    value = _get_file_config(section,key)
    
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
            value = defalut_config[section].get(key, None)
            
    else:  #各资源类配置
        if value == None:
            value = defalut_config['source'][section].get(key, None)  
        
    #格式化地址
    if key == 'download_path' and value != None:
        value = format_path_str(value)
        
    #格式化时间
    if key == 'start_date' and value != None:
        value = format_time_str(value, '%Y-%m-%d')
    
    #print('{}:{}'.format(key,value))
    return value


#配置设置
def set_config(section='main', **kwargs):
    # 检查section是否合法
    if section not in allowable_config_sections:
        raise Exception("section名称不正确："+section)
    
    config_file = defalut_config['main']['config_file']
    comfig_file_expand = os.path.expanduser(config_file)
       
    config = configparser.ConfigParser()
    config.read(comfig_file_expand)

    if section not in config:
        config.add_section(section)  #添加section

    for k,v in kwargs.items():    
        if k not in allowable_config_keys:
            raise Exception("键名称不正确："+k)
        if k == 'download_path':  #如果如下载路径，检查目录并创建
            v = format_path_str(v, mkdir=True)
        config.set(section, k, v)

    with open(comfig_file_expand, 'w') as configfile:
        config.write(configfile) 
    
    print('配置写入成功。')


# 获取数据库名称配置
def get_db_name(section):
    download_path = get_config('main','download_path') 
    download_path = os.path.expanduser(download_path)

    source_postfix = defalut_config['source'][section]['postfix']  #数据源对应的后缀
    data_kind = defalut_config['data']
    db_name = {} 
    for k in data_kind.keys():
        db_name[k]=download_path+k+source_postfix + '.db'

    return db_name


        
        
# -----------------------------------------------------------------------------
# 配置类 Config
# -----------------------------------------------------------------------------

class Config:
   
    download_path = get_config('main','download_path')  #获取下载位置配置，默认用户目录下：'~/dfdata/'
    log_level = get_config('main','log')     #获取打印信息日志等级，默认正常等级，'normal'
    log = log_level
    allowable_arg_names = allowable_arg_names   #允许函数输入的参数名称，不在这列表中报参数错误。
    source_names = list(defalut_config['source'].keys())   #所有数据源名称列表，如['tushare','collect']
    data_kinds = list(defalut_config['data'].keys())       #所有数据类型列表，如['futures','stocks']
   
    def __init__(self, source_kind):
        
        #初始化时，判断输入数据源名称是否合法，
        if source_kind not in Config.source_names:
            raise ValueError("数据源名称错误!") 
            
        self.name = source_kind+" config"
        self.kind = source_kind
        self.db = get_db_name(source_kind)     #数据源的默认数据库地址名称
        self.source_config = defalut_config['source'][source_kind]
        self.strftime_format = self.source_config['strftime_format']  #数据源的时间转字符串格式
        self.today_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))  #今天日期
        self.today =  self.today_time.strftime(self.strftime_format)  #今天日期字符串，按数据源对应格式
        self.yesterday = (self.today_time - datetime.timedelta(days=1)).strftime(self.strftime_format) #昨天日期字符串，按数据源对应格式
        self.start_date = self._get_start_date()  #获取设置开始时间字符串, 按数据源格式
        self.end_date_time = self.today_time
        self.end_date = self.today
        self.exchange = self._get_exchange()
        self.sleep_time = defalut_config['main']['sleep_time']
        
        
    def _get_exchange(self):
        exchange = {}
        for k, v in self.source_config.items():
            try:
                exchange[k] = v["exchange"]
            except:
                pass

        return exchange

    # 获取下载的开始时间
    # 取main和source中最大值
    def _get_start_date(self):
        start_date_in_main = get_config('main','start_date')
        start_date_in_source = get_config(self.kind,'start_date')
        start_date = start_date_in_main
        if start_date_in_source != None:
            start_date = max(start_date_in_main, start_date_in_source)
        #格式化字时间
        start_date = format_time_str(start_date, self.strftime_format)
        return start_date

    
class Source(Config):
    """   
    暂时没用
    """
    def __init__(self, source_kind, ):
        self.kind = source_kind
        self.name = self.kind
        

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
        
    def __init__(self,input_dict={}, source_kind=None, data_kind=None, table=None, function_kind='save'):
        """
        初始化
        input_dict (dict) : 用户输入的参数
        source_kind (str) ：数据源类别
        data_kind (str) ：数据类别，如'futures', 'stock'
        table (str) : 表名称
        function_kind (str) : 函数类别，默认'save'，参数缺失时使用默认填充，'read',有些参数不使用默认值如start_date 
        """
        KeyWords.source_kind=source_kind
        KeyWords.table=table
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
        log.debug('表名称：table = ' + str(table))  
        
     
  
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
            db_name = KeyWords.config.db[KeyWords.data_kind]
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
    
    
    def _get_func_start_date(self):
        start_date_in_config = KeyWords.config.start_date
        try:
            #查看数据源的对应函数中是否有设置start_date
            start_date = KeyWords.config.source_config[KeyWords.data_kind][KeyWords.table]['start_date']
            start_date = format_time_str(start_date, KeyWords.config.strftime_format)
            start_date = max(start_date, start_date_in_config) 
        except:
            #start_date = getattr(KeyWords.config, 'start_date')
            start_date = KeyWords.config.start_date
            
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
    
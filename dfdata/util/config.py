#配置文件
import datetime
import configparser
import os

# 数据源collect配置
collect_config = {  
    'postfix':'_ct',  #后缀，用于数据库名称
    'strftime_format':'%Y-%m-%d', # 日期转时间格式
}  

# 数据源tushare配置  
tushare_config = { 
    'postfix':'_ts',  #后缀，用于数据库名称
    'strftime_format':'%Y%m%d',
    'futures':{ #期货设置
        'exchange' : {  #期货交易所代码和名称字典
            'CZCE':'郑州商品交易所',
            'SHFE':'上海期货交易所',
            'DCE':'大连商品交易所',
            'CFFEX':'中国金融期货交易所',
            'INE':'上海国际能源交易所'
        },
        'start_date' : '19900101',
        
    },
     'stock':{ #股票设置
     },

}

# 数据源jqdata配置
jqdata_config = {  
    'postfix':'_jq',  #后缀，用于数据库名称
    'strftime_format':'%Y-%m-%d',
    'id' : '', #用户账号
    'password' : '',  #用户密码     
}


    
# 默认配置
defalut_config = {  
    
    #主要配置
    'main':{  
        'download_path' : '~/dfdata/',  #下载位置，默认在用户目录下的dfdata目录
        'config_file' : "~/configs/dfdata.ini",    #配置文件，默认在用户目录configs/dfdata.ini
        'log': 'normal',   #配置输出信息等级，默认等级normal
        'start_date' : datetime.datetime.strptime('1900-01-01',"%Y-%m-%d"),  #开始时间
        'allowable_arg_names' : [  #允许的参数名称, 如果没出现在该列表，会抛出参数错误异常
                'source', 'db', 'table','start_date','end_date',
                'fields','sql', 'limit',    #sql查询参数-通用
                'exchange', 'code',         #sql查询参数-字段
                'log',
                'is_open',     #tushare中
                ],
    },
   
    # 数据配置
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
        



#配置读取
def get_config(section='main', key=None):  
    config_file = defalut_config['main']['config_file']
    config_file_expand = os.path.expanduser(config_file) #连接展开
    config = configparser.ConfigParser()
    config.read(config_file_expand)

    if key == None:
        return config[section]

    try:
        #print('{}:{}'.format(section,key))
        value = config[section][key]
        #print('got in config value: {}'.format(value))
    except:
        value = defalut_config[section][key]

    if key == 'download_path':
        value = format_path_str(value)
    
    #print('{}:{}'.format(key,value))
    return value


#配置设置
def set_config(section='main', **kwargs):
    config_file = defalut_config['main']['config_file']
    comfig_file_expand = os.path.expanduser(config_file)
       
    config = configparser.ConfigParser()
    config.read(comfig_file_expand)

    if section not in config:
        config.add_section(section)  #添加section

    for k,v in kwargs.items():    
        if k == 'download_path':  #如果如下载路径，检查目录并创建
            v = format_path_str(v, mkdir=True)
        config.set(section, k, v)

    with open(comfig_file_expand, 'w') as configfile:
        config.write(configfile)  


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
    allowable_arg_names = defalut_config['main']['allowable_arg_names']    #允许函数输入的参数名称，不在这列表中报参数错误。
    source_names = list(defalut_config['source'].keys())   #所有数据源名称列表，如['tushare','collect']
    data_kinds = list(defalut_config['data'].keys())       #所有数据类型列表，如['futures','stocks']
    start_date = get_config('main','start_date')      #获取默认开始时间，缺失时才使用
   
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
        self.start_date_time = Config.start_date
        self.start_date = self.start_date.strftime(self.strftime_format)  #默认开始时间，缺失时才使用，按数据源对应格式
        self.end_date_time = self.today_time
        self.end_date = self.today
        self.exchange = self._get_exchange()
        
        
    def _get_exchange(self):
        exchange = {}
        for k, v in self.source_config.items():
            try:
                exchange[k] = v["exchange"]
            except:
                pass

        return exchange
    



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
    2. 用户通过config函数的设置
    3. 函数中定义的参数
    4. defalut_config字典默认定义
    
    """  
        
    def __init__(self,input_dict={}, source_kind=None, data_kind=None, table=None, function_args=None):
        """
        初始化
        input_dict (dict) : 用户输入的参数
        source_kind (str) ：数据源类别
        data_kind (str) ：数据类别，如'futures', 'stock'
        table (str) : 表名称
        function_args (dict) : 函数中定义的参数，可以覆盖defalut_config参数中的值
        """
        KeyWords.source_kind=source_kind
        KeyWords.table=table
        KeyWords.data_kind=data_kind
        KeyWords.source_config = Config(source_kind)
        KeyWords.source = KeyWords.source_config
        KeyWords.function_args = function_args
        
        
        for k,v in input_dict.items():      
            #处理输入参数字典, 按键和数据源类型，返回对应格式的值
            v = self._input_parser(k,v) 
            
            #初始化参数字典
            if isinstance(v,dict):
                self.__setitem__(k,KeyWords(v,KeyWords.source_kind, KeyWords.data_kind, KeyWords.table, function_args=None))
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
        log.debug('函数字典：function_args = ' + str(function_args))  
        
     
  
    #初始化参数字典
    def __setitem__(self,k,v):
        dict.__setitem__(self,k,v)
        dict.__setattr__(self,k,v)
        
        
    #处理输入参数字典
    def _input_parser(self, k, v):   
        
        # 检测参数名称是否合法"
        if k not in KeyWords.source_config.allowable_arg_names:
            raise Exception('输入参数名称错误: {}'.format(k))
        
        #按键和数据源类型，返回对应格式的值"
        date_key_list = ['start_date', 'end_date']
        if k in date_key_list:
            v= format_time_str(v, KeyWords.source_config.strftime_format)  
        return v
                
            
        
    #未输入参数，获取设置参数或默认参数
    # 默认返回None
    def __missing__(self,k):       
        if k == "db" :
            db_name = KeyWords.source_config.db[KeyWords.data_kind]
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
        
        key_list = ['today','today_str','start_date','end_date',
               'log',  ]
        if k in key_list:
            value = getattr( KeyWords.source_config, k)
            self.__setitem__(k, value)
            return value
        
        return None
    
    __setattr__=__setitem__
    __getattr__=__missing__     
    
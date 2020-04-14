#配置文件
import configparser
import os

#默认配置
#配置存储位置，用户目录的configs目录中的dfdata.ini
CONFIGS_FILE = os.path.expanduser("~/configs/dfdata.ini")
DEFAULT_DOWNLOAD_PATH = os.path.expanduser('~/dfdata/')

#配置文件的section和section后面属性都大写

#路径配置
#setion = path
# download_path下载位置配置


#聚宽jqdata配置名称
#setion = jqdata
#id 用户名
#password 用户密码


# block_size  #下载时分块的大小，默认一次获取3000个

#配置读取
def get_config(section, name):
    config = configparser.ConfigParser()
    config.read(CONFIGS_FILE)
    vaule = config[section][name]
    return vaule

#配置设置
def set_config(section, name, value):
    config = configparser.ConfigParser()
    config.read(CONFIGS_FILE)
    
    if section not in config:
        config.add_section(section)  #添加section
        
    if section == 'path':
        value = os.path.expanduser(value)
        
    config.set(section, name, value)
    with open(CONFIGS_FILE, 'w') as configfile:
        config.write(configfile)  

        
        
# 获取数据库名称配置
def get_db_name(section):
    try:
        download_path = get_config('path','download_path')  
    except:
        download_path = DEFAULT_DOWNLOAD_PATH
        
    defalut_db_name = defalut_config[section]['db_name']
    db_name = {}    
    for k, v in defalut_db_name.items():
        db_name[k]=download_path+v
                
    return db_name    
    





# 默认配置
defalut_config = {
    'path':{
        'download_path' : DEFAULT_DOWNLOAD_PATH,  #下载位置
        'config_file' : CONFIGS_FILE             #配置文件
    },
    'table_name':{    #数据名称表配置
        'futures_contract' : 'futures_contract',
        'futures_daily' : 'futures_daily',
    },
    'tushare':{    # 数据源tushare配置
        'db_name':{   
            'futures_db_name' : 'futures_ts.db',
            'stock_db_name' : 'stock_ts.db', 
        },
    
    },
    'jqdata':{  #数据源jqdata配置
        'id' : '', #用户账号
        'password' : '',  #用户密码
        'db_name':{
            'futures_db_name' : 'futures_jq.db',
            'stock_db_name' : 'stock_jq.db', 
        },
        
    },
    
}
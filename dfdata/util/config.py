#配置文件

import configparser
CONFIGS_FILE = "~/.dfdata_config"
JQDATA_SETION = "JQDATA"

#聚宽配置文件
def config_jqdata(ID='',Password='',once_count=None,):
    config = configparser.ConfigParser()
    
    #账号密码
    if ID != '':config[JQDATA_SETION] = {'ID': ID}  
    if Password != '':config[JQDATA_SETION] = {'Password':Password}
        
    #每次获取的数据量
    if limit == None:
        try:
            config.read(CONFIGS_FILE)
            limit = config[JQDATA_SETION]["sub_count"]
        except:
            limit = 3000
     
    config[JQDATA_SETION] = {'sub_count':sub_count}
    
    #保存到文件
    with open(CONFIGS_FILE, 'w') as configfile:
        config.write(configfile)      
    
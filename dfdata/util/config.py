#配置文件
import configparser
import os

#配置存储位置，用户目录的configs目录中的dfdata_config.ini
CONFIGS_FILE = os.path.expanduser("~/configs/dfdata_config.ini")

#配置文件的section和section后面属性都大写
#聚宽配置名称
JQDATA_SETION = "JQDATA"
jqdata_id = "ID"              #用户名称
jqdata_password = "PASSWORD"  #用户密码
BLOCK_SIZE = "BLOCK_SIZE"     #下载时分块的大小，默认一次获取3000个

#读取配置
def get_config(setion, name):
    setion = setion.upper()
    name = name.upper()
    config = configparser.ConfigParser()
    config.read(CONFIGS_FILE)
    vaule = config[setion][name]
    return vaule

#聚宽配置文件
def config_jqdata(ID='',Password='',block_size=None):
    config = configparser.ConfigParser()
         
    #每次获取的数据量
    if block_size == None:
        try:
            config.read(CONFIGS_FILE)
            block_size = config[JQDATA_SETION][BLOCK_SIZE]
        except:
            block_size = 3000
     
    config[JQDATA_SETION] = {
        jqdata_id: ID,
        jqdata_password:Password,
        BLOCK_SIZE:block_size,
    }
    
    #保存到文件
    with open(CONFIGS_FILE, 'w') as configfile:
        config.write(configfile)      


# dfdata/default_config.py
# dfdata默认配置

download_path = '~/data/'  #下载位置，默认在用户目录下的dfdata目录
config_file = "~/configs/dfdata.ini"    #配置文件，默认在用户目录configs/dfdata.ini
log = 'normal'   #配置输出信息等级，默认等级normal
start_date = '1900-01-01'  #开始时间
sleep_time = 0.5  


# 可用配置文件键值对的键名称列表。防止用户输错    
allowable_config_keys = [ 
    'download_path', 'config_file', 'log', 'start_date','sleep_time',
    'id', 'password',
]

# 允许的参数名称, 如果没出现在该列表，会抛出参数错误异常。
allowable_arg_names = [ 
        'source', 'db', 'table','start_date','end_date','sleep_time',
        'fields','sql', 'limit',    #sql查询参数-通用
        'exchange', 'code',  'trade_date',       #sql查询参数-字段
        'log',
        'is_open',     #read_data的date_table
        ]
    
#-------------------------------------------------------------------------------
### 函数默认参数配置  
#-------------------------------------------------------------------------------

stock_daily = {
    'start_date' : '19960101',
}
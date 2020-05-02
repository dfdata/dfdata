import requests
import lxml
from lxml import etree
import pandas as pd
from dfdata.source.collect.futures import consts as cs

"""
郑州商品交易所官网：http://www.czce.com.cn/
---
期货每日行情从20050509开始
第一种链接，20050509-20100824
http://www.czce.com.cn/cn/exchange/jyxx/hq/hq20050509.html
http://www.czce.com.cn/cn/exchange/jyxx/hq/hq20100824.html
第二种链接，20100825-20150930
http://www.czce.com.cn/cn/exchange/2010/datadaily/20100825.htm
http://www.czce.com.cn/cn/exchange/2015/datadaily/20150930.htm
第三种链接，20151001-至今
http://www.czce.com.cn/cn/DFSStaticFiles/Future/2015/20151008/FutureDataDaily.htm
http://www.czce.com.cn/cn/DFSStaticFiles/Future/2020/20200227/FutureDataDaily.htm

---
期权每日行情 从20170419开始
http://www.czce.com.cn/cn/DFSStaticFiles/Option/2017/20170419/OptionDataDaily.htm
http://www.czce.com.cn/cn/DFSStaticFiles/Option/2020/20200227/OptionDataDaily.htm
"""
def get_zce_daily(date=None, type="future"):
    """
    获取郑州商品交易所每日行情
    
    """
    if date < '20050509':
        return
    elif '20050509' <= date and date <= '20100824':
        url = cs.ZCE_DAILY_1_URL % date
        tabel_xpath = cs.ZCE_DAILY_1_XPATH
    elif '20100825' <= date and date <= '20150930':
        url = cs.ZCE_DAILY_2_URL % (date[:4], date)
        tabel_xpath = cs.ZCE_DAILY_2_XPATH
    else:
        url = cs.ZCE_DAILY_3_URL % (date[:4], date)
        tabel_xpath = cs.ZCE_DAILY_3_XPATH
        
    my_headers = dict(list(cs.SIMPLE_HEAD.items())+list(cs.ZCE_ADD_HEAD.items()))
    #print("url={}\n xpath={}\n headers={}".format(url, tabel_xpath, my_headers)) 
    
    res = requests.get(url, headers=my_headers) 
    if res.status_code == 404:
        print('不存在')
        return
    res_elements = etree.HTML(res.content.decode('utf-8'))  #如果不以utf-8解码，中文会显示乱码
    tables = res_elements.xpath(tabel_xpath)
    table = etree.tostring(tables[0])
    df = pd.read_html(table, header=0)[0]
    return df


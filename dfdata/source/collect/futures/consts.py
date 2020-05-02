
ZCE_DAILY_1_URL = 'http://www.czce.com.cn/cn/exchange/jyxx/hq/hq%s.html'
ZCE_DAILY_2_URL = 'http://www.czce.com.cn/cn/exchange/%s/datadaily/%s.htm'
ZCE_DAILY_3_URL ='http://www.czce.com.cn/cn/DFSStaticFiles/Future/%s/%s/FutureDataDaily.htm'
ZCE_DAILY_1_XPATH = '//table[@cellspacing="1"]'
ZCE_DAILY_2_XPATH = '//table[@id="senfe"]'
ZCE_DAILY_3_XPATH = '//table[@id="tab1"]'

SIMPLE_HEAD = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
}

ZCE_ADD_HEAD = {
    'Referer': 'http://www.czce.com.cn/cn/jysj/mrhq/index.htm',
}

myheaders = {
    'Accept': '*/*', 
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'Connection': 'keep-alive',
    'Referer': 'http://www.czce.com.cn/cn/jysj/mrhq/index.htm',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
}
import requests
import json
import time
import datetime
import csv

#获取市场每日成交概况原始数据,默认股票市场
#如获取2019年12月02日股票成交概况 get_market_json("2019-12-02") 
#如获取12日基金成交概况 get_market_json("2019-12-12","fund") 
def get_market_json(date='', market='stock'):
    marketinfo = {
        'stock':{ #股票市场信息
            'refere':'http://www.sse.com.cn/market/stockdata/overview/day/',
            'prodType':'gp'
        },
        'fund':{ #基金市场信息
            'refere':'http://www.sse.com.cn/market/funddata/overview/day/',
            'prodType':'jj'
        }
    }

    myheaders = { #请求headers
        'Accept': '*/*', 
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
        'Connection': 'close',   #默认keep-alive
        'Host': 'query.sse.com.cn',
        'Referer': marketinfo[market]['refere'],
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }

    searchDate = date  #下载的日期
    timestamp = int(time.time()*1000)  #时间戳
    urlparams = { #链接参数
        'jsonCallBack':'jsonpCallback72081',
        'searchDate':searchDate,
        'prodType':marketinfo[market]['prodType'],
        '_':timestamp
    }
    url = 'http://query.sse.com.cn/marketdata/tradedata/queryNewTradingByProdTypeData.do'
    #使用Requests中的get()方法
    try:
        res = requests.get(url, headers=myheaders, params=urlparams)  
        if res.ok: #成功访问
            json = res.content.decode()
            jsontext=json.strip('jsonpCallback72081').strip('(').strip(')') #取出json内容
            return jsontext
    except Exception as e:
        print('Error here:\t', e)

#从返回值中提取整理数据
def json_parser(jsondata):
    
    typeDict = { #产品类型转换
        #摘自官网 
        #注：本栏目发布的股票合计数据自2019年7月22日起，只包含主板A、主板B、科创板的数据，将不包含股票回购数据。
        '1':"stock_A", #1为股票主板B
        '2':"stock_B", #2为股票主板B
        '12':"stock_old", #12为股票(旧)，包含主板A、主板B、科创板，股票回购的数据
        '40':"stock", #40为股票，包含主板A、主板B、科创板的数据
        '48':"stock_STAR", #48为科创板
        '43':"stock_repurchase", #43为股票回购
        '90':"90", #90表示股票的什么类型？,也没数据       
    }
    

    resdict = json.loads(jsondata)  #json内容转换为python字典
    resdict_result = resdict['result']  #取出返回字典的result的值
    result = [] #函数返回值
    for item in resdict_result:
        if len(item['trdAmt1'])!=0: #如果成交额不为空，就保存这条数据
            #每行数据：日期(searchDate),产品类型(productType),挂牌数量(istVol),市价总值(亿元)(marketValue1),
            #           流通市值(亿元)(negotiableValue1),成交金额(亿元)(trdAmt1),成交量(亿股)(trdVol1),成交笔数(万笔)(trdTm1),
            #            平均市盈率(倍)(profitRate1),换手率(%)(exchangeRate)
            row = (item['searchDate'], typeDict[item['productType']], item['istVol'], item['marketValue1'], item['negotiableValue1'], item['trdAmt1'], item['trdVol1'], item['trdTm1'], item['profitRate1'], item['exchangeRate'])
            #print(row)
            result.append(row)
    return result

#下载数据
def download_marketdata(startdate, enddate, market='stock'):
    date_current = datetime.datetime.strptime(startdate, "%Y-%m-%d")  
    date_end = datetime.datetime.strptime(enddate, "%Y-%m-%d")
    data = [('date','productType','istVol','marketValue','negotiableValue','trdAmt','trdVol1','trdTm','profitRate','exchangeRate')] #结果列表,先加入表头
    while date_current<=date_end:
        if date_current.isoweekday() != 6 and date_current.isoweekday() != 7 :    #星期六，星期天没数据，不用处理
            daydata_json = get_market_json(date_current)  #获取当天原始数据
            result = json_parser(daydata_json)   #提取数，保存到变量result
            data.extend(result)       #将处理后的数据，添加到data列表后面
            print(str(date_current)+'当天处理完成！')
            time.sleep(0.5)   #设置休眠时间，减小服务器压力
        date_current+=datetime.timedelta(days=1)
        
    #print(data)
    
    #将结果列表data保存到cvs中
    filename = 'dayily_'+market+'_'+startdate+'_'+enddate+'.csv'
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)

if __name__ == '__main__':
    download_marketdata('2019-11-10','2019-11-30')

# dfdata
dfdata 用于下载金融数据。将数据源的数据保存到本地，默认sqlite数据库。

## 安装
```
pip install dfdata
```

## 使用


下载tushare pro 数据源为例。使用`pip install tushare`安装好tushare，再设置一次tushare的token，它会保存在用户目录下tk.csv。
```
import tushare as ts
ts.set_token('your_tushare_token')  
```
接下载可以使用dfdata下载和读取数据。
```
import dfdata as dd

# 下载期货日线行情
dd.save_futures_daily(source='tushare')

# 读取期货日线行情
dd.read_futures_daily(source='tushare')
```

更多使用方法见文档：http://dfdata.org/
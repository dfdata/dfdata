## 安装sphinx
`pip install sphinx`

## 安装设置主题 pydata-sphinx-theme

### 通过pip安装
`pip install pydata-sphinx-theme`

Sphinx的conf.py文件设置:    
html_theme = "pydata-sphinx-theme" 

### 下载导入
pydata-sphinx-theme仓库：https://github.com/pandas-dev/pydata-sphinx-theme.git   
下载后将pydata-sphinx-theme/pydata-sphinx-theme文件夹放入docs/source/_themes

Sphinx的conf.py文件设置:    
html_theme = "pydata-sphinx-theme"    
html_theme_path = ["_themes", ]    

参考：https://sphinx-rtd-theme.readthedocs.io/en/stable/installing.html#via-git-or-download


## 生成网页

删除已生成html
`make clean`

生成html
`make html`


## 在JupyterLab中渲染页面
`from IPython.display import IFrame
IFrame(src='https://www.baidu.com', sandbox="allow-scripts", width=1000, height=600)`


## 服务器上显示
在docs文件夹下，建立server.py文件，写如下代码，启动一个简单的web服务器。
```
import sys
import os
import mimetypes
from wsgiref import simple_server, util

path = os.path.join(os.getcwd(), 'build/html')
#print(path)

def app(environ, respond):

    fn = os.path.join(path, environ['PATH_INFO'][1:])
    if '.' not in fn.split(os.path.sep)[-1]:
        fn = os.path.join(fn, 'index.html')
    type = mimetypes.guess_type(fn)[0]

    if os.path.exists(fn):
        respond('200 OK', [('Content-Type', type)])
        return util.FileWrapper(open(fn, "rb"))
    else:
        respond('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'404 Not Found']

#启动服务器，传入函数app
httpd = simple_server.make_server('', 8081, app)
print("Serving HTTP on port 8081...")
```

然后启动web服务器，浏览器中打开ip:8081即可看到文档：
 `python server.py`
 
## 使用web服务器软件Nginx部署

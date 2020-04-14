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
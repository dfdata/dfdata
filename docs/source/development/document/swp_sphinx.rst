
================================
Sphinx教程
================================


安装
---------------------------------

使用pip安装
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
可以使用pip安装，如下::

    pip install -U sphinx
    
使用docker安装
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sphinx的官方docker镜像有两个：

* sphinxdoc/sphinx，常用的Sphinx镜像。
* sphinxdoc/sphinx-latexpdf，比较大，主要使用LaTeX构建PDF的Sphinx镜像。

先安装好docker，然后直接使用docker run命令自动下载镜像并启动容器。如下::

    #从sphinxdoc/sphinx镜像启动一个名称为sphinx的容器并后台运行，挂载当前目录下的project/docs目录到容器docs目录。
    docker run -itd -v $PWD/project/docs:/docs --name sphinx sphinxdoc/sphinx  /bin/bash
    #进入sphinx容器
    docker exec -it sphinx /bin/bash
    #运行sphinx-quickstartx脚本生成Sphinx默认模板，
    sphinx-quickstart
    #修改首页index.rst等
    #，仅需运行make html而不需要使用sphinx-build生成。
    make html


入门
---------------------------------
    
编写内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
sphinx默认使用reStructuredText 


构建网页
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

由sphinx-quickstart脚本创建的make.bat使生成网页更容易，仅需运行make html而不需要使用sphinx-build生成。如下::

    make html

清除已构建的网页使用::

    make clean
    
    
主题
---------------------------------
    
安装主题
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


主题设置
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


扩展
---------------------------------

常用内置扩展
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
autodoc
~~~~~~~~~~~~~
autodoc扩展能够提取源代码中的文档字符串(DocStrings)生成文档，文档字符串需要按reStructuredText格式编写，可以使用所有常用的Sphinx标记。一般搭配napoleon扩展一起使用。


详细信息阅读：
* https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
* https://www.sphinx.org.cn/usage/extensions/autodoc.html

napoleon
~~~~~~~~~~~~~
napoleon扩展使Sphinx能够解析NumPy和Google风格的文档字符串。

详细信息阅读：
* https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#module-sphinx.ext.napoleon
* https://www.sphinx.org.cn/usage/extensions/napoleon.html

第三方扩展
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



参考文献
---------------------------------
* `sphinx.org.cn：sphinx翻译文档 <https://www.sphinx.org.cn/>`_


网站
---------------------------------
* `sphinx官网 <https://www.sphinx-doc.org>`_
* `sphinx入门 <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_
* `sphinx文档 <https://www.sphinx-doc.org/en/master/contents.html>`_


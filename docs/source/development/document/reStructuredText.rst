=======================
reStructuredText教程
=======================

标题
-----------------------
标题用使用文字和特殊的标点符号下划线来创建的（上划线是可选的），符号的长度需要不小于文字。
可以用作标题使用的标点符号：! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ` { | } ~ 


一篇文档使用格式如下::

    =================
    一级标题 
    =================

    1 二级标题
    ----------------
    
    1.1 三级标题 
    ^^^^^^^^^^^^^^^^
    
    1.2 三级标题 
    ^^^^^^^^^^^^^^^^
    
    2 二级标题
    ----------------
    
    2.1 三级标题 
    ^^^^^^^^^^^^^^^^

=================
一级标题 
=================


1 二级标题
---------------
    
1.1 三级标题 
^^^^^^^^^^^^^^^^

1.1 三级标题 
^^^^^^^^^^^^^^^^
    
2 二级标题
----------------
    
2.1 三级标题 
^^^^^^^^^^^^^^^^

2.2 三级标题 
^^^^^^^^^^^^^^^^


Normally, there are no heading levels assigned to certain characters as the
structure is determined from the succession of headings.  However, this
convention is used in `Python's Style Guide for documenting
<https://docs.python.org/devguide/documenting.html#style-guide>`_ which you may
follow:

* ``#`` with overline, for parts
* ``*`` with overline, for chapters
* ``=``, for sections
* ``-``, for subsections
* ``^``, for subsubsections
* ``"``, for paragraphs

Of course, you are free to use your own marker characters (see the reST
documentation), and use a deeper nesting level, but keep in mind that most
target formats (HTML, LaTeX) have a limited supported nesting depth.




超链接
-----------------------

外部链接
~~~~~~~~~~~~~~


内部链接
~~~~~~~~~~~~~~


参考文献
-----------------------

* https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
* https://docutils.sourceforge.io/docs/user/rst/quickref.html
* https://docutils.sourceforge.io/docs/user/rst/quickstart.html
* http://www.pythondoc.com/sphinx/rest.html
* https://www.jianshu.com/p/1885d5570b37

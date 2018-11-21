# -*- coding: utf-8 -*-
# @Date     : 2018-11-07 17:09:10
# @Author   : Jimy_Fengqi (jmps515@163.com)
# @Link     : https://blog.csdn.net/qiqiyingse
# @Version  : V1.0
# @pyVersion: 3.6

# -*- coding: utf-8 -*-  
from scrapy import cmdline  
  
name = 'xuanshu'  
cmd = 'scrapy crawl {0}'.format(name)  
cmdline.execute(cmd.split())
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-11 00:00:06
# @Author  : Jimy_Fengqi (jmps515@163.com)
# @Link    : https://blog.csdn.net/qiqiyingse/
# @Version : $Id$

import scrapy
import re
from scrapy.http import Request
from xuanshu.items import XuanshuItem


class Myspider(scrapy.Spider):
	name = "xuanshu"
	allowed_domains = ["3uww.cc"]
	main_url = "https://www.3uww.cc/"
	shuku_url_base='https://www.3uww.cc/shuku/0_0_0_0_default_0_%s.html'

	txt_base_url='https://txt.3uww.cc/home/down/txt/id/%s'
	zip_base_url='https://txt.3uww.cc/home/down/zip/id/%s'
	

	def start_requests(self):
		print('hello world')
		yield Request(self.main_url+'shuku.html',self.parse)
	def parse(self, response):
		print(response.url)
		max_page=response.xpath('//*[@id="taoshumain"]/div[31]/a[11]/@href').extract_first()
		max_page=max_page.split('.')[-2].split('_')[-1]
		print(max_page)
		max_novel_num=response.xpath('//*[@class="bookstorbt1"]/span/text()').extract_first()
		print('max_novel_num=(%s)' % max_novel_num)
		for page_num in range(1,int(max_page)):
		#for page_num in range(1,2):
			new_url=self.shuku_url_base % str(page_num)
			print(new_url)
			yield Request(new_url,self.get_novel)
	def get_novel(self,response):
		novel_contents=response.xpath('//*[@class="storelistbt5"]/ul')
		print('每一页有%d 个小说' %  len(novel_contents))
		
		item=XuanshuItem()
		for content in novel_contents.xpath('li[2]'):
			#downloadNum=content.xpath('span/text()').extract_first()
			
			novelname	=content.xpath('a[2]/@title').extract_first()
			novelurl	=content.xpath('a[2]/@href').extract_first()
			author 		=content.xpath('p[1]/a[1]/text()').extract_first()
			noveltype 	=content.xpath('p[1]/a[3]/text()').extract_first()
			downloadNum =content.xpath('span/text()').extract_first()
			downloadNum=downloadNum.split('：')[-1].strip()
			novelid 	=novelurl.split('.')[-2].split('/')[-1]
			novelsize 	=content.xpath('p[3]/text()').extract_first()
			txtdownload=self.txt_base_url % (novelid)
			zipdownload=self.zip_base_url % (novelid)
			item['novelname']=novelname
			item['author']=author
			item['downloadNum']=downloadNum
			item['novelurl']=novelurl
			item['novelid']=novelid
			item['novelsize']=novelsize
			item['noveltype']=noveltype
			item['txtdownload']=txtdownload
			item['zipdownload']=zipdownload
			#print(novelname,author,novelid,noveltype,novelsize,downloadNum,novelurl)
			#print(txtdownload,zipdownload)
			yield item
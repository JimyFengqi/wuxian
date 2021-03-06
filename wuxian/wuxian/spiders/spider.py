# -*- coding: utf-8 -*-
# @Date     : 2018-11-07 17:11:13
# @Author   : Jimy_Fengqi (jmps515@163.com)
# @Link     : https://blog.csdn.net/qiqiyingse
# @Version  : V1.0
# @pyVersion: 3.6

#coding:utf-8
import scrapy
import re
from scrapy.http import Request
from wuxian.items import WuxianItem

class Myspider(scrapy.Spider):
	name = "wuxian"
	allowed_domains = ["555x.org"]
	main_url = "http://www.555x.org/"
	shuku_url_base='http://www.555x.org/shuku/0_0_0_0_default_0_%s.html'
	downloadpage_url_base='http://www.555x.org/down/%s.html'
	txt_base_url='http://down.555x.org/txt/%s/%s.txt'
	zip_base_url='http://down.555x.org/zip/%s/%s.zip'

	def start_requests(self):
		yield Request(self.main_url+'shuku.html',self.parse)
	def parse(self, response):
		#print(response.url)
		max_page=response.xpath('//*[@class="yemian"]/ul/li[12]/span/strong[1]/text()').extract_first()
		print(max_page)

	
		for page_num in range(1,int(max_page)):
		#for page_num in range(1,2):
			new_url=self.shuku_url_base % str(page_num)
			print(new_url)
			yield Request(new_url,self.get_novel)
	def get_novel(self,response):
		novel_contents=response.xpath('//*[@class="xiashu"]/ul')
		print('每一页有%d 个小说' %  len(novel_contents))
		item=WuxianItem()
		for content in novel_contents:
			novelname=content.xpath('li[5]/a/text()').extract_first()
			if novelname:
				novelname=novelname.split('《')[1].split('》')[0]
			author=content.xpath('li[4]/text()').extract_first()
			downloadNum=content.xpath('li[1]/text()').extract_first()
			novelurl=content.xpath('li[5]/a/@href').extract_first()
			novelid=novelurl.split('txt')[1].split('.')[0]
			novelsize=content.xpath('li[2]/text()').extract_first()
			noveltype=content.xpath('li[7]/a/text()').extract_first()
			txtdownload=self.txt_base_url % (novelid,novelname)
			zipdownload=self.zip_base_url % (novelid,novelname)

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
			
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



from xuanshu.items import XuanshuItem
from xuanshu import settings
import os,sys
import urllib,requests
import pymongo

class PymongoDataSave():
	def __init__(self):
		self.client=pymongo.MongoClient()
		self.xuanshu=self.client.xuanshuxiaoshuo

	def saveDataInDB(self,db,datalist,):
		print(datalist)
		table=self.xuanshu[db]
		table.insert_one(datalist)


class XuanshuPipeline(object):
	def __init__(self):
		self.mg=PymongoDataSave()
		self.s=requests.session()

	def process_item(self, item,spider):
		dir_path="%s/" % (settings.NOVEL_STORGE)
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		if isinstance(item,XuanshuItem):
			novelname=item['novelname']
			author=item['author']
			downloadNum=item['downloadNum']
			noveltype=item['noveltype']
			novelurl=item['novelurl']
			novelid=item['novelid']
			novelsize=item['novelsize']
			txtdownload=item['txtdownload']
			zipdownload=item['zipdownload']
			#print(novelname,author,novelid,noveltype,novelsize,downloadNum,novelurl)
			#print(txtdownload,zipdownload)

			novelpath=dir_path+'/'+noveltype
			print ('novelpath = %s' % novelpath)
			if not os.path.exists(novelpath):
				os.makedirs(novelpath)
			a={
				'novelname':novelname,
				'author':author,
				'downloadNum':downloadNum,
				'noveltype':noveltype,
				'novelurl':novelurl,
				'novelid':novelid,
				'novelsize':novelsize,
				'txtdownload':txtdownload,
				'zipdownload':zipdownload
			}

			self.mg.saveDataInDB(noveltype,a)
			
			'''
			contentpath=novelpath+'/'+novelname+'.txt'
			if not os.path.exists(contentpath):
				self.save_file_with_response(contentpath,txtdownload)
			'''
		return item
	#url为网址
	def save_file_with_url(self,filename, url):
		urllib.request.urlretrieve(url,filename)

	def save_file_with_response(self,filename, url):
		def get_url_response(url):
			headers ={
		            'Accept': '*/*',
		            'Accept-Encoding': 'identity;q=1, *;q=0',
		            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
		            'Connection': 'keep-alive',
		            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',		 
		            'Range': 'bytes=0-'
		           }
			#r = s.get(url, headers=headers, stream=True)
			#r = s.get(url, stream=True)
			r = self.s.get(url)
			#print(r)
			return r
		with open(filename, 'wb') as fd:
		    for chunk in get_url_response(url).iter_content(chunk_size=128):
	        	fd.write(chunk)
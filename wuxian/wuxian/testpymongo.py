# -*- coding: utf-8 -*-
# @Date     : 2018-11-08 11:29:27
# @Author   : Jimy_Fengqi (jmps515@163.com)
# @Link     : https://blog.csdn.net/qiqiyingse
# @Version  : V1.0
# @pyVersion: 3.6
import re
import os
import sys
import pymongo
import requests

class PymongoDataSave():
	def __init__(self,data='test'):
		self.s=requests.session()
		self.client=pymongo.MongoClient()

		self.wuxian=self.client.wuxianxiaoshuo
		
	def saveDataInDB(self,db,datalist,):
		print(datalist)
		table=self.wuxian[db]
		table.insert_one(datalist)

	def getData(self,db):
		table=self.wuxian[db]
		datalist=table.find()
		#print('类型【%s】 有小说【%d】部' % (db,len(datalist)))
		for item in datalist:
			novelname=item['novelname']
			author=item['author']
			downloadNum=item['downloadNum']
			noveltype=item['noveltype']
			novelurl=item['novelurl']
			novelid=item['novelid']
			novelsize=item['novelsize']
			txtdownload=item['txtdownload']
			zipdownload=item['zipdownload']
			print(novelname,author,novelid,noveltype,novelsize,downloadNum,novelurl)

			novelpath='无限小说'+'/'+noveltype
			if not os.path.exists(novelpath):
				os.makedirs(novelpath)
			contentpath=novelpath+'/'+novelname+'.txt'
			if not os.path.exists(contentpath):
				self.save_file_with_response(contentpath,txtdownload)

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
	def print_database_and_table_name(self):
		for database in self.client.database_names():
			if 'wuxianxiaoshuo' == database:
				for table in self.client['wuxianxiaoshuo'].collection_names():
					#print('table [%s] is in database [%s]' %(table,database))
					print('"%s",'% table)
			#for table in self.client[database].collection_names():
			#	print('table [%s] is in database [%s]' %(table,database))



class Handletxt():
	def __init__(self):
		self.novelpath='无限novel\\东方玄幻'

	def getfilelist(self,path):
		filelist=[]
		for file in os.listdir(path):
			novel=path+'\\'+file
			new_path=path+'_new'
			if not os.path.exists(new_path):
				os.mkdir(new_path)
			new_novel=new_path+'\\'+file
			self.delete_other(novel,new_novel)
			filelist.append(novel)
		return filelist


		'''
		for parent,dirnames,filenames in os.walk(path):

			#case 1:
			for dirname in dirnames:
				print("parent folder is:" + parent)
				print("dirname is:" + dirname)
			#case 2
			for filename in filenames:
				print("parent folder is:" + parent)
				print("filename with full path:"+ os.path.join(parent,filename))
		'''
	def delete_other(self,path,newpath):
		try:
			fread=open(path,'r',encoding='gbk')
			f=fread.readlines()
			fread.close()
			if '用户上传之内容开始' in f[1] and '用户上传之内容结束' in f[-2]:
				f=f[2:-2]

			os.remove(path)
			fwrite=open(newpath,'w',encoding='utf-8')
			fwrite.writelines(f)
			fwrite.close()

		except Exception as e1:
			print('%s  gbk编码格式不能处理' % path)
			print(e1)
			fread.close()
			try:
				fread=open(path,'r',encoding='utf-8')
				f2=fread.readlines()
				fread.close()
				if '用户上传之内容开始' in f2[1] and '用户上传之内容结束' in f2[-2]:
					f=f[2:-2]
				os.remove(path)
				fwrite=open(newpath,'w',encoding='utf-8')
				fwrite.writelines(f2)
				fwrite.close()
			except Exception as e2:
				print('%s 编码格式有问题，gbk和utf-8都不能处理'% path)	
				print(e2)
				return

			return

		#print('%s  处理结束' % path)


mymongo=PymongoDataSave()

mymongo.print_database_and_table_name()
mymongo.getData('东方玄幻')

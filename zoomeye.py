# -*- coding: utf-8 -*

import os
import json
import math
import censys
import pymongo
import shodan
import requests
from requests.auth import HTTPBasicAuth
from censys import *
from pymongo import MongoClient
from time import sleep

class zoomeye():


	port = [102,502,5007,9600,44818]

	def __init__(self):
		url = "https://api.zoomeye.org/user/login"
		data = {}
		data['username'] = 'youngcraft@qq.com'
		data['password'] = 'cnxc2008ymgk'
		r = requests.post(url, json=data)
		#print r.text
		token = json.loads(r.text)
		#print token[u'access_token']
		token_ring = 'JWT ' + token[u'access_token']
		self.token = token_ring
		self.url = url

		con = MongoClient(host='127.0.0.1',port=27017)
		db = con.get_database('IOT')
		self.col = db.get_collection('zoomeye')

	def main(self):
		# 100 page for use
		for port_item in self.port:
			url = 'https://api.zoomeye.org/host/search?query=port:%d' % port_item
			r = requests.get(url,headers = {'Authorization':self.token})
			content = json.loads(r.content)
			#get the result,if result i None,choose to pass
			if len(content[u'matches']) and content[u'total'] :
				#----------------------------
				print '%s :matching item is %d' % (port_item, len(content[u'matches']))
				page_total = int(math.ceil(content[u'total']/10))
				for page_id in range(1,page_total):
					req_url = 'https://api.zoomeye.org/host/search?query=port:%d&page=%d' % (port_item,page_id)
					r = requests.get(req_url, headers={'Authorization': self.token})
					inner =  json.loads(r.content)
					print 'length of the result is '
					print len(inner[u'matches'])
					for node in inner[u'matches']:
						self.col.insert(node)
			else:
				print 'not success,get None result'
		
	def GetResourceInfo(self):
		url = 'https://api.zoomeye.org/resources-info'
		r = requests.get(url,headers = {'Authorization':self.token})
		return r.text

class shandon():
	port = [102, 502, 5007, 9600, 44818]

	def __init__(self):
		con = MongoClient(host='127.0.0.1', port=27017)
		db = con.get_database('IOT')
		self.col = db.get_collection('shandon')
		SHODAN_API_KEY = "W0Dtsj8tFmMRxdLNSkK8Uwvg8Ma7ebi8 "

		self.api = shodan.Shodan(SHODAN_API_KEY)



	def main(self):
		# 100 page for use
		for node in self.port:
			try:
				# Search Shodan
				results = self.api.search('port:%d' % node)
				# Show the results
				print 'Results found: %s' % results['total']
				for result in results['matches']:
					print result
					self.col.insert_one(result)
			except shodan.APIError, e:
				print 'Error: %s' % e


class DiTng():

	port = [102, 502, 5007, 9600, 44818]

	def __init__(self):
		pass

	def main(self):
		pass

class Censys():
	port = [u'102/s7', u'502/modbus']

	def __init__(self):
		con = MongoClient(host='127.0.0.1', port=27017)
		db = con.get_database('IOT')
		self.col = db.get_collection('censys')

		self.API_URL = "https://www.censys.io/api/v1"
		self.UID = "55a9a367-a2c6-4bf9-b2fb-054d93541af6"
		self.SECRET = "mKnixOhpaLqXEtdkgtd0IMTJXd97toP3"

		#self.UID = "85e64536-7534-4177-8c72-9a383bf01f12"
		#self.SECRET = "9hCyul4KXJKXieyXeGIFT0lr04rbN9yQ"

	def search(self):

		pages =2 #float('inf')
		page = 1

		for port_item in self.port:
			params = {u'query': 'protocols:"102/s7"',u'page': page}
			print type(params)
			url = self.API_URL + "/search/ipv4"
			res = requests.post(url, data=json.dumps(params), auth=(self.UID, self.SECRET))
			payload = res.json()
			metadata = payload['metadata']
			metadata['_id'] = 'metadata:' + port_item
			print metadata
			self.col.replace_one({'_id':metadata['_id']},metadata,upsert=True)
			#---------------------------
			#insert the metadata result
			print 'Total page is %d' % payload['metadata']['pages']
			for r in payload['results']:
				r['_id']= r['ip']+':'+ port_item
				self.col.delete_one({'_id':r['_id']})
				self.col.insert(r,check_keys=False)
			sleep(10)
			#----------------------------
			for page_item in range(2,payload['metadata']['pages']):
				params = {u'query': 'protocols:"102/s7"', u'page': page_item}
				res = requests.post(url, data=json.dumps(params), auth=(self.UID, self.SECRET))
				payload = res.json()
				for r in payload['results']:
					r['_id'] = r['ip'] + ':' + port_item
					self.col.delete_one({'_id': r['_id']})
					self.col.insert( r, check_keys=False)
				sleep(10)


	def search2(self):
		api = censys.ipv4.CensysIPv4(api_id=self.UID, api_secret=self.SECRET)
		res = api.search({'protocols':"102/s7"})
		matches = res['metadata']['count']
		pageNum = matches / 100
		if matches % 100 != 0:
			pageNum = pageNum + 1



if __name__ == '__main__':
	x = Censys()
	x.search()






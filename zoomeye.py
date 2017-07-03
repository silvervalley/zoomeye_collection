#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import json
import math
import pymongo
import shodan
import requests
from requests.auth import HTTPBasicAuth

from pymongo import MongoClient

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

	def __init__(self):
		pass

	def main(self):
		pass



if __name__ == '__main__':
	x = zoomeye()
	x.main()






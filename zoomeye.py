import os 
import requests
import json

from requests.auth import HTTPBasicAuth

class zoomeye():

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

	def main(self):
		# 100 page for use
		for p_item in range(1,10000):
			url = 'https://api.zoomeye.org/host/search?query=port:80 p=%d' % p_item
			r = requests.get(url,headers = {'Authorization':self.token})
			#print r.content
			content = json.loads(r.content)
			print content[u'matches'][0][u'ip']
			#----
			print 1


if __name__ == '__main__':
	x = zoomeye()
	x.main()






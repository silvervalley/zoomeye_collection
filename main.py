#coding=utf-8

import pymongo

from mongoengine import *
from pymongo import MongoClient



class checktable():

    def __init__(self):
        con = MongoClient(host='127.0.0.1', port=27017)
        self.db = con.get_database('IOT')

    def parser(self):
        maintable = self.db.get_collection('main')
        col_name = ['diting-result','censys','shodan','zoomeye']

        for c in col_name:
            name = self.db.get_collection(c)
            for node in name.find({'ip':'217.109.105.26'}):
                ip = node['ip']
                if maintable.find_one({'ip':node['ip'],'port':node['port']}):
                    #print 'get %d result from maintable' % len(maintable.find({'ip':node['ip']}))
                    xpoint = maintable.find({'ip':node['ip'],'port':node['port']})
                    #updating the data
                    for item in xpoint:
                        try:
                            if c in item.keys():
                            #if item key field contain diting data
                                if node['_id'] not in item[c]:
                                    item[c].append(node['_id'])
                                else:
                                    pass
                            else:
                                #if diting not in key field
                                ex = []
                                ex.append(node['_id'])
                                item['diting'] = ex
                        except Exception as e:
                            print e
                else:
                    a = {}
                    a['_id'] = node['ip'] + ':' + str(node['port'])
                    a['ip'] = node['ip']
                    a['port'] = node['port']
                    a[c] = [node['_id']]
                    maintable.insert(a,check_keys=False)


if __name__ == '__main__':
    x = checktable()
    x.parser()



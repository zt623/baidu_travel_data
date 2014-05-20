# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib, json, os
from db_manager import DBManager
from decorators import async

db = DBManager()

def get_travel_location(address):
	address = urllib.quote(address)
	url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=FD09ed40290e289709ffe50b546c3a23' % address
	r=urllib.urlopen(url).read()
	rlt = json.loads(r)
	return rlt

def insert_travel_location(jingdian_id,province,place,name):
	print str(jingdian_id),str(province),str(place),str(name),'...'
	try:
		address = str(province+place+name)#str(place+name) if str(name).find(str(place)) < 0 else str(name)
		rlt = get_travel_location(address)
		if rlt['status'] == 0:
			location_lng = rlt['result']['location']['lng']
			location_lat = rlt['result']['location']['lat']
			sql = '''INSERT INTO dim_travel_location(`jingdian_id`,`search_value`,`location_lng`,`location_lat`) 
			VALUES(%s,'%s','%s','%s')''' % (str(jingdian_id),address,location_lng,location_lat)
			db.executeNonQuery(sql)
		else:
			f = open('error.txt','a')
			f.write(str(province)+' ==== '+str(place)+' ==== '+str(name)+'\n')
			f.close()
		print 'finished!'
	except Exception,e:
		print e
	
if __name__ == '__main__':

	sql = '''SELECT a.`id`,a.`province`,a.`place`,a.`name` 
		FROM dim_travel AS a
		WHERE NOT EXISTS
		(
		SELECT 1
		FROM dim_travel_location AS l
		WHERE l.jingdian_id = a.`id`
		)
		ORDER BY a.`id` LIMIT 0, 1000'''
	result = db.executeQuery(sql)

	import time
	print 'here we go ...'

	filename = r'error.txt'
	if os.path.exists(filename):
		os.remove(filename)

	try:
		for row in result:
			insert_travel_location(row['id'],row['province'],row['place'],row['name'])
	except Exception,ex:
		print ex
		time.sleep(0.5)
		insert_travel_location(row['id'],row['province'],row['place'],row['name'])

# 青海湖黑马河乡
# 青海倒淌河
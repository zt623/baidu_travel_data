# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import re, os

import urllib, json


def wget_new_travel_info(level,place_url,place,filename):
	print 'get %d %s %s' % (level,place_url,place)
	
	url = 'http://lvyou.baidu.com/destination/ajax/jingdian?format=ajax&surl=%s' % place_url 
	url = url + '&cid=1&pn=%d&t=0'
	page_index = 1
	wget = True
	citys = []
	while wget:
		try:
			content = urllib.urlopen(url % page_index).read()
		except UnicodeError,e:
			print e
			content = json.dumps({'data':{'scene_list':[]}})
		except Exception,ex:
			print ex
			import time
			time.sleep(1)
			content = urllib.urlopen(url % page_index).read()

		a = json.loads(content)
		data = a['data']
		if data['scene_list'] == []:
			wget = False
		for j in data['scene_list']:
			city = {}
			city['url'] = j['surl']
			city['name'] = j['sname']
			citys.append(city)

			content = j['ext']['more_desc'].replace("'","''")
			picture = '' if j.get('cover') is None else j['cover']['full_url']
			sql = "INSERT INTO travel_data(`level`,`place`,`name`,`desc`,`picture`) VALUES(%d,'%s','%s','%s','%s');" % (level,place,j['sname'],content,picture)
			
			output = open(filename, 'a')
			output.write(sql+'\n')#j['sname'],j['ext']['more_desc'],j['cover']['full_url']
			output.close()
		page_index = page_index + 1

	print 'finished'
	return citys


ls = [
{'url':'qinghai','name':'青海'},{'url':'ningxia','name':'宁夏'},{'url':'neimenggu','name':'内蒙古'},
{'url':'gansu','name':'甘肃'},{'url':'shaanxi','name':'陕西'},{'url':'shanxi','name':'山西'},
{'url':'sichuan','name':'四川'},{'url':'guizhou','name':'贵州'},{'url':'guangxi','name':'广西'},
{'url':'hunan','name':'湖南'},{'url':'hubei','name':'湖北'},
{'url':'jiangxi','name':'江西'},{'url':'hainan','name':'海南'},
{'url':'anhui','name':'安徽'},{'url':'jilin','name':'吉林'}
{'url':'henan','name':'河南'},{'url':'hebei','name':'河北'},
{'url':'liaoning','name':'辽宁'},{'url':'heilongjiang','name':'黑龙江'},
{'url':'shandong','name':'山东'},{'url':'jiangsu','name':'江苏'},
{'url':'fujian','name':'福建'},{'url':'yunnan','name':'云南'},
{'url':'zhejiang','name':'浙江'},
{'url':'aomen','name':'澳门'}
] # just sample

if __name__ == '__main__':
	for l in ls:
		filename = r'.\data\travel_%s.txt' % l['url']
		if os.path.exists(filename):
			os.remove(filename)
		datas = wget_new_travel_info(1,l['url'],l['name'],filename)
		for i in datas:
			wget_new_travel_info(2,i['url'],i['name'],filename)

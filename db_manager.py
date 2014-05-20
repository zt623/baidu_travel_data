# -*- coding: utf-8 -*-

import MySQLdb
'''
from sae.const import (MYSQL_HOST, MYSQL_HOST_S,
    MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
)
'''

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'user_name'
MYSQL_PASS = 'user_pwd'
MYSQL_DB = 'db_name'


class DBManager:
	def __init__(self):
		self.MYSQL_HOST = MYSQL_HOST
		self.MYSQL_USER = MYSQL_USER
		self.MYSQL_PASS = MYSQL_PASS
		self.MYSQL_DB = MYSQL_DB
		self.MYSQL_PORT = int(MYSQL_PORT)
	
	def __getCursor(self):
		if not hasattr(self,"_conn"):
			self._conn = MySQLdb.connect(self.MYSQL_HOST, self.MYSQL_USER, self.MYSQL_PASS,self.MYSQL_DB, port=int(self.MYSQL_PORT),charset="utf8")
		cursor = self._conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
		return cursor

	def __closeCursor(self,cursor):
		self._conn.commit()
		cursor.close()
		if hasattr(self,"_conn"):
			self._conn.close()
			del self._conn

	def escape_string(self,content):
		content = MySQLdb.escape_string(content)
		return content

	# 执行一条sql语句返回受影响行数
	def executeNonQuery(self,sql):
		cur = self.__getCursor()
		cur.execute(sql)
		rowCount = cur.rowcount
		self.__closeCursor(cur)
		return rowCount

	def executeNonQueries(self,sqls):
		cur = self.__getCursor()
		for sql in sqls:
			#sql = self.escape_string(sql)
			print sql
			cur.execute(sql)
		self.__closeCursor(cur)

	def executeQuery(self,sql):
		cur = self.__getCursor()
		cur.execute(sql)
		retult = list(cur.fetchall())
		self.__closeCursor(cur)
		return retult

	def executeQueries(self,*sqls):
		results = []
		cur = self.__getCursor()
		for sql in sqls:
			cur.execute(sql)
			results.append(list(cur.fetchall()))
		self.__closeCursor(cur)

		return results

	def executeScalar(self,sql):
		pass

	def executeProc(self,procName,args):
		results = []
		cur = self.__getCursor()
		cur.callproc(procName,args)

	def executeMany(self,sql,args):
		cur = self.__getCursor()
		result = cur.executemany(sql, args)
		self.__closeCursor(cur)
		return result

	def executeTrans(self,*sqls):
		results = []
		cur = self.__getCursor()
		for sql in sqls:
			sql = sql.strip()
			cur.execute(sql)
			if sql[0:6].upper() == "SELECT":
				results.append(list(cur.fetchall()))
		self.__closeCursor(cur)
		return results

	
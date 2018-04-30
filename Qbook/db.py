# -*- coding: utf-8 -*-
import sys

import pymysql
import traceback
sys.path.append("..")


class DB:
    def __init__(self):
        try:
            self.conn = pymysql.connect('localhost', 'root', 'mysql', 'qbook',charset='utf8')
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        except:
            print 'mysql connect is error'
            exit()


    def get_info(self,id):
        sql = """SELECT id,title,url,type FROM book WHERE id=1 AND id>{} """.format(id)
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.conn.commit()
            return res
        except Exception, e:
            print e
            print 'get min_id is error'

    def yz_info(self,url):
        sql = """SELECT id FROM book WHERE url='%s' """%url
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.conn.commit()
            return res
        except Exception, e:
            print e
            print 'get min_id is error'


    def Install(self, title, url, type):
        sql = """INSERT INTO book (title,url,type)
                             VALUES (%s,%s,%s)"""
        try:
            self.cursor.execute(sql,(title, url, type))
            self.conn.commit()
        except:
            print u"更新失败"
            self.conn.rollback()

    def __del__(self):
        self.cursor.close()
        self.conn.close()



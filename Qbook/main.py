# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree
import re, threading, requests, traceback, os
from db import DB

L = threading.Lock()


class Qbook(object):
    def __init__(self):
        self.sion = requests.session()
        self.db = DB()
        try:
            self.sion.get("http://www.quanshuwang.com/")
        except:
            pass

    def XPATH(self, url, xp):
        while 1:
            try:
                res = self.sion.get(url).content
                html = etree.HTML(res)
                res = html.xpath(xp)
                return res
            except:
                pass

    def Classify(self):  # 分类处理
        try:
            name = self.XPATH('http://www.quanshuwang.com/', '//ul[@class="channel-nav-list"]//a/text()')[
                   :-1]  # 分类名字
            href = self.XPATH('http://www.quanshuwang.com/', '//ul[@class="channel-nav-list"]//@href')[:-1]  # 分类链接
            for n, h in zip(name, href):
                n.decode("utf8")
                t = threading.Thread(target=self.stert_thread, args=(h, n))
                t.start()
        except:
            pass

    def stert_thread(self, h, n):
        page_list = self.XPATH(h, '//a[@class="last"]/@href')[0]  # 每一页链接
        tpye_page_url = re.findall(r'([_\d]+)', page_list)[0]
        tpye_page = tpye_page_url.split("_")
        url_typt = tpye_page[0]
        page = tpye_page[1]
        for page_num in range(1, int(page) + 1):
            page_url = "http://www.quanshuwang.com/list/%s_%s.html" % (url_typt, page_num)
            book_list = self.XPATH(page_url, '//a[@class="clearfix stitle"]/@href')  # 每一本书的链接列表、
            name_list = self.XPATH(page_url, '//a[@class="clearfix stitle"]/@title')  # 每一本书的链接列表、
            for bookred, b_name in zip(book_list, name_list):
                book_red_link = self.XPATH(bookred, '//a[@class="reader"]/@href')[0]
                print b_name
                L.acquire()
                yz = self.db.yz_info(book_red_link)
                if not yz:
                    self.db.Install(b_name, book_red_link, n)
                # self.Sec_page(book_red_link, b_name)
                L.release()  # 释放锁

    def getbody(self, urlx, title, b_name):
        try:
            res = self.sion.get(urlx)
        except:
            while 1:
                try:
                    res = self.sion.get(urlx)
                except:
                    pass
        html = res.content.decode('gbk')
        sector = etree.HTML(html)
        body = sector.xpath('//div[@id="content"]/text()')

    def Sec_page(self, url, b_name):
        while 1:
            try:
                res = self.sion.get(url)
                html = res.content.decode('gbk')
                sector = etree.HTML(html)
                content = sector.xpath('//div[@class="clearfix dirconone"]//a/@href')
                title_list = sector.xpath('//div[@class="clearfix dirconone"]//a/text()')
                for urlx, title in zip(content, title_list):
                    self.getbody(urlx, title, b_name)
                break
            except:
                pass



if __name__ == '__main__':
    start = Qbook()
    start.Classify()

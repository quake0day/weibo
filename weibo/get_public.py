import urllib,urllib2
import re
import BeautifulSoup
import MySQLdb

class Weibo:
    def __init__(self):
        url = 'http://www.weibo.com/'
        response = urllib2.urlopen(url)
        doc = response.read()
        self.soup = BeautifulSoup.BeautifulSoup(''.join(doc))
        self.conn = \
                MySQLdb.connect(host='localhost',user='root',passwd='chensi', \
                db='weibo_add')

    def draw_info_from_whole_item(self,items):
       #print item
        info = {}
        for item in items:
            for tag in item:
                if isinstance(tag,BeautifulSoup.NavigableString):
                    if len(tag) > 1:
                        content = tag.string[1:]
                if isinstance(tag,BeautifulSoup.Tag):
                    if tag.name == 'a':
                        uid = tag['uid']
            try:
                info[uid] = content
            except Exception,e:
                pass
        return info

    def get_whole_itemt(self):
        self.soup.prettify()
        self.items = self.soup.findAll("div",{"class":"twit_item_content"})
        #print len(self.itemt)
        #for tag in self.items:
         #   if isinstance(tag,BeautifulSoup.NavigableString):
          #      if len(tag) > 1:
           #         print tag.string[1:]
            #if isinstance(tag,BeautifulSoup.Tag):
             #   if tag.name == 'a':
              #      print tag['uid']
        return self.items

    def store_item_info(self):
        info = self.draw_info_from_whole_item(self.get_whole_itemt())
        self.cur = self.conn.cursor()
        if info is not None:
            while len(info) > 0:
                k = info.popitem()
                uid = k[0]
                content = k[1]
                sql = "insert into `choose` (`uid`,`content`) VALUES('"\
                        + uid + "','" + content + "')"
		try:
                  self.cur.execute(sql)
                  self.conn.commit()
  		except Exception,e:
		  pass
        self.cur.close()


        



weibo = Weibo()
weibo.store_item_info()


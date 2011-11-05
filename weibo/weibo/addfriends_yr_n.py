import unittest
from weibopy.auth import OAuthHandler 
from weibopy.api import API
import sys
import MySQLdb
from time import sleep
from types import *
from trim import trim

consumer_key = '3572381405'
consumer_secret = 'cbfea68b35a3e9aa19914092a60a6575'
token_pre = []
token_last = []

# Load configuration file

fd = open(sys.path[0]+"/users.cs","r")
users = fd.readlines()
for user in users:
    token_pre.append(user.split(",")[0])
    token_last.append(user.split(",")[1][0:-1])

""" For New User ONLY !"""
#auth = OAuthHandler(consumer_key,consumer_secret)
#auth.setToken(token,tokenSecret)
#auth_url = auth.get_authorization_url()
#print 'Please authorize: ' + auth_url
#verifier = raw_input('PIN: ').strip()
#auth.get_access_token(verifier)

#api = API(auth)


""" Begin """
class test(unittest.TestCase):

    consumer_key = '3572381405'
    consumer_secret = 'cbfea68b35a3e9aa19914092a60a6575'

    def __init__(self):
        self.conn = \
                MySQLdb.connect(host='localhost',user='root',passwd='chensi',db='weibo_add')
        """ constructor """
        

    def getAtt(self,key):
        try:
            return self.obj.__getattribute__(key)
        except Exception,e:
            print e
            return ''

    def getAttValue(self,obj,key):
        try:
            return obj.__getattribute__(key)
        except Exception,e:
            print e
            return ''

    def auth(self):
        self.auth = OAuthHandler(self.consumer_key,self.consumer_secret)
        auth_url = self.auth.get_authorization_url()
        print 'Please authorize: ' + auth_url
        verifier = raw_input('PIN').strip()
        self.auth.get_access_token(verifier)
        self.api = API(self.auth)

    def setToken(self,token,tokenSecret):
        self.auth = OAuthHandler(self.consumer_key,self.consumer_secret)
        self.auth.setToken(token,tokenSecret)
        self.api = API(self.auth)

    def friends(self):
        timeline = self.api.friends()
        for line in timeline:
            self.obj = line
            fid = self.getAtt("id")
            name = self.getAtt("screen_name")
            print "friends --"+ str(fid) + ":" + name

    def public_timeline(self):
        magic_num = 0
        timeline = self.api.public_timeline(count=2,page=1)
        for user in timeline:
            #self.obj = line
            #mid = self.getAtt("id")
            self.obj = user
            user_profile = self.getAtt("user")
            self.obj = user_profile
            uid = self.getAtt("id")
            followers_count = self.getAtt("followers_count")
            friends_count = self.getAtt("friends_count")
            if followers_count != 0:
                magic_num = friends_count/followers_count
            #text = self.getAtt("text")
        return uid,magic_num
    
    def test_junk(self,id):
        sql = "select jid from junkid"
        self.cur = self.conn.cursor()
        junk_set_n = self.cur.execute(sql)
        junk_set = self.cur.fetchall()
        for jid in junk_set:
            if int(jid[0]) == int(id):
                self.cur.close()
                return True
        self.conn.commit()
        self.cur.close()
        return False

    def create_friendship(self,id):
        user = self.api.create_friendship(id)
        self.obj = user
        uid = self.getAtt("id")
        sql = "insert into `baby_info_yr` (`kid`) VALUES('"\
                + str(uid) + "')"
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()
        self.cur.close()
        return 0 

    def user_timeline(self):
        timeline = self.api.user_timeline(count=200,page=4)
        for line in timeline:
            self.obj = line
            mid = self.getAtt("id")
            text = self.getAtt("text")
            created_at = self.getAtt("created_at")
            self.cur = self.conn.cursor()
            sql = "insert into `data` (`mid`,`datetime`,`text`) VALUES('"\
                    + str(mid) + "','" + str(created_at)+"','"+trim(text)+"')"

            self.cur.execute(sql)

            self.conn.commit()
            self.cur.close()

            
            print "user_timeline:::"+str(mid)+":"+str(created_at)+":"+text
    
    

if __name__ == '__main__':
    test = test()
    config_id = int(sys.argv[1])
    test.setToken(token_pre[config_id],token_last[config_id])
    data_set = test.public_timeline()
    print data_set
    if (test.test_junk(str(data_set[0])) is not True) and (data_set[1] >= 1):
        test.create_friendship(data_set[0])



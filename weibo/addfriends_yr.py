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
token = 'dd4494c20bc2b2b382c5a82954a0645d'
tokenSecret = 'c8c1a02ec9624a51a69fdbf6d9c80bd8'



auth = OAuthHandler(consumer_key,consumer_secret)
auth.setToken(token,tokenSecret)
auth_url = auth.get_authorization_url()
print 'Please authorize: ' + auth_url
verifier = raw_input('PIN: ').strip()
auth.get_access_token(verifier)

#api = API(auth)

#status = api.update_status(status="OK Cool", lat='12.33',longs='12.2')
#print status.id
#print status.text
class test(unittest.TestCase):

    consumer_key = '3572381405'
    consumer_secret = 'cbfea68b35a3e9aa19914092a60a6575'
    #token = 'dd4494c20bc2b2b382c5a82954a0645d' #tokenSecret = 'c8c1a02ec9624a51a69fdbf6d9c80bd8'

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
        timeline = self.api.public_timeline(count=2,page=1)
        for user in timeline:
            #self.obj = line
            #mid = self.getAtt("id")
            self.obj = user
            user_profile = self.getAtt("user")
            self.obj = user_profile
            uid = self.getAtt("id")

            #text = self.getAtt("text")
        return uid
    
    def test_junk(self,id):
        sql = "select jid from junkid"
        self.cur = self.conn.cursor()
        junk_set_n = self.cur.execute(sql)
        junk_set = self.cur.fetchall()
        for jid in junk_set:
            print jid[0]
            if int(jid[0]) == int(id):
                print "hiaa"
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
    
    

test = test()
test.setToken('bda9d13bd2ed3168135db7f6ab414845','014805318b9181ed17020ca145954621')
kid = test.public_timeline()

if test.test_junk(str(kid)) is not True:
    if str(kid) != '2147483647':
        test.create_friendship(kid)


import unittest
from weibopy.auth import OAuthHandler 
import time
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
        judge_res = 0
        timeline = self.api.public_timeline(count=1,page=1)
        for line in timeline:
            self.obj = line 
            text = self.getAtt("text")
            judge_res = judge_res + self.judge_text(text)
        for user in timeline:
            magic_num = 0
            self.obj = user
            user_profile = self.getAtt("user")
            self.obj = user_profile
            uid = self.getAtt("id")
            description = self.getAtt("description")
            followers_count = self.getAtt("followers_count")
            friends_count = self.getAtt("friends_count")
            if followers_count != 0:
                magic_num = friends_count/followers_count
                judge_res = judge_res + self.judge_magic_num(magic_num)
            #text = self.getAtt("text")
        return uid,judge_res
    
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
        sql = "insert into `baby_info` (`kid`) VALUES('"\
                + str(uid) + "')"
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()
        self.cur.close()
        return 0 

    def judge_magic_num(self,magic_num):
        if magic_num >= 1 and magic_num <= 10:
            return 0
        return 1

    def judge_text(self,text):
        count_at = text.split("@")
        if len(count_at) > 2:
            return 1
        return 0

    def show_analysis(self,uid):
        dataset = self.api.get_user(uid)
        self.obj = dataset
        followers = self.getAtt("followers_count")
        friends = self.getAtt("friends_count")
        self.cur = self.conn.cursor()
        sql = "insert into `data` (`uid`,`followers`,`friends`,`time`) VALUES(\
                '" + str(uid) + "','" + str(followers) + "','" + str(friends) +\
                "','" + str(int(time.time())) + "')"
        self.cur.execute(sql)
        self.conn.commit()
        self.cur.close()
        print friends



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
    uid = int(sys.argv[2])
    test.setToken(token_pre[config_id],token_last[config_id])
    test.show_analysis(uid)



import urllib, urllib2,cookielib
import Cookie

  
url =\
"http://www.weibo.cn/dpool/ttt/home.php?uid=2262463192&vt=3"
response = urllib2.urlopen(url)
doc = response.read()
print doc
#print resp.read()


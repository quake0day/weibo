#encoding=utf-8
import mechanize 
import cookielib
# Browser 
br = mechanize.Browser()
# Cookie Jar 
cj = cookielib.LWPCookieJar() 
br.set_cookiejar(cj)
# Browser options 
br.set_handle_equiv(True) 
br.set_handle_gzip(True) 
br.set_handle_redirect(True) 
br.set_handle_referer(True) 
br.set_handle_robots(False)                               #这个是设置对方网站的robots.txt是否起作用。
# Follows refresh 0 but not hangs on refresh > 0 
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
# Want debugging messages? 
#br.set_debug_http(True) 
#br.set_debug_redirects(True) 
#br.set_debug_responses(True)
# User-Agent (this is cheating, ok?) 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]                    #设置ua 

# Open some site, let’s pick a random one, the first that pops in mind: 

r = br.open('http://www.weibo.cn/dpool/ttt/home.php?uid=2262463192&vt=3')
html = r.read()
# Show the source 
print html
#f = open('./kk','wr')
#f.write(html)



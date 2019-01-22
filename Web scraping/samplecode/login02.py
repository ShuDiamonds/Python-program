# coding: utf-8

# login to twitter

import urllib
import urllib2
import cookielib

def build_request(path, data=None):
    req = urllib2.Request("https://twitter.com" + path)
    if data:
        req.add_data(urllib.urlencode(data))
    # Firefox 3.6.3 for Windows
    req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729)")
    return req
    
    
class TwitterLoginHandler(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        self.build_opener()
        
    def build_opener(self):
        self.opener = urllib2.build_opener()
        # cookie
        self.opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    def login(self):
        # /sessions に 以下のパラメータを送信
        #   - session[username_or_email] : username
        #   - session[password]          : password
        data = {
            "session[username_or_email]": self.username,
            "session[password]": self.password,
        }
        conn = self.opener.open(build_request("/sessions", data))
        cont = conn.read()
        f = open('login.html', 'w')
        f.write(cont)
        f.close()
        conn.close()
    
    def logout(self):
        # /sessions/destroy
        self.opener.open(build_request('/logout'))
    
    def request(self, req):
        if type(req) == str:
            return self.opener.open("https://twitter.com" + req)
        else:
            return self.opener.open(req)
        


username = raw_input("username: ")
password = raw_input("password: ")
hand = TwitterLoginHandler(username, password)
hand.login() 

conn = hand.request("/following")

f = open("out.html", "w")
f.write(conn.read())
f.close()

hand.logout()

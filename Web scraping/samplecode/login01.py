#! /usr/bin/python3.2
# python3 sample script: http post; logging in hatena
# ref: http://docs.python.org/py3k/library/urllib.request.html
# ref: http://diveintopython3.org/files.html
import urllib
import urllib.request # opener
import urllib.parse # urlencode
import http
import http.cookiejar

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

u, p = 'usernmae','********'
post = {
    'name': u,
    'password': p
}
data = urllib.parse.urlencode(post).encode('utf-8')

conn = opener.open('http://www.hatena.ne.jp/login', data)
ofs = open('out.html', 'w', encoding='utf-8')
ofs.write(conn.read().decode('utf-8'))
ofs.close()

conn = opener.open('http://d.hatena.ne.jp/%s/edit' % u)
ofs = open('out2.html', 'w', encoding='euc-jp')
ofs.write(conn.read().decode('euc-jp'))
ofs.close()

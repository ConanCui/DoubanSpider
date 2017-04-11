#coding=utf-8
import sys
import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
import StringIO
from PIL import Image

#-------------------------------------------------------------------log in part
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36'}
url = 'https://www.douban.com/accounts/login'
logginPage=''
keepRequest=1
while keepRequest==1:
    try:
        req=urllib2.Request(url,headers=headers)
        logginPage=urllib2.urlopen(req,timeout=1).read()
    except:
        print 'request again'
    else:
        keepRequest=0
#print logginPage
soup = BeautifulSoup(logginPage)
imgUrl=soup.find(attrs={'id':'captcha_image'})['src']
captcha_id=soup.find(attrs={'name':'captcha-id'})['value']
buffer=urllib2.urlopen(imgUrl).read()
im=Image.open(StringIO.StringIO(buffer))
im.show()
captcha_solution= raw_input("Captcha is:")
data={'source':'simple',
      'redir':'https://www.douban.com/people/158524999/',
      "form_email":'15608232038',
      'form_password':'727158nan',
      'captcha-solution':captcha_solution,
      'captcha-id':captcha_id,
      'user_login':'登录'
      }
post_data=urllib.urlencode(data)
keepRequest=1
while keepRequest==1:
    try:
        req=urllib2.Request(url,post_data,headers)
        confirmUrl=urllib2.urlopen(req,timeout=1).geturl()
    except:
        print 'request again'
    else:
        keepRequest=0
        if confirmUrl=='https://www.douban.com/people/77250418/contacts':
            print 'sign in success'
        else:
            print 'shit! Please run again'
            sys.exit(0)

BaseUrl = 'https://movie.douban.com/tag/'
# BaseUrl = 'http://blog.csdn.net/shanzhizi/article/details/50903748'
headers = BrowserHeaders()
# request = urllib2.Request(BaseUrl, headers=headers)
# response = urllib2.urlopen(request)
# soup = BeautifulSoup(response, "lxml")
response = requests.get(BaseUrl,headers = headers,proxies = proxies)
soup = BeautifulSoup(response.text, 'lxml')

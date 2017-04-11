# -*- coding:utf-8 -*-

import re
import sys
import csv
import time
import urllib
import urllib2
import requests
from bs4 import BeautifulSoup
import os

reload(sys)
sys.setdefaultencoding('utf-8')


def BrowserHeaders():
    head = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/' \
           '537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
    headers = {'User-Agent': head}
    return headers


def GetTag():
    BaseUrl = 'https://movie.douban.com/tag/'
    headers = BrowserHeaders()
    try:
        request = urllib2.Request(BaseUrl)
        response = urllib2.urlopen(request)
        soup = BeautifulSoup(response, "lxml")
    except Exception, e:
        print "maybe blocked!"
        return False
    for items in soup.find_all('table', {'class': 'tagCol'}):
        taglist = re.findall(r'<td><a href="/tag/.*?">(.*?)</a><b>.*?</b></td>', str(items))
        for tag in taglist:
            GetFilmPage(tag, 5)
    return True


def GetFilmPage(TagName, pangeNumber):
    '''
    :param TagName: movie type
    :param pangeNumber:
    :return: movie'url in pangeNumber in movie type
    '''
    TagUrl = 'https://movie.douban.com/tag/{tag}?start={start}&type=T'
    headers = BrowserHeaders()
    for pages in range(pangeNumber):
        print ("    crawling page%d... in %s" % (pages + 1, TagName))
        # time.sleep(6)
        startNum = pages * 20
        Tagurl = TagUrl.format(start=startNum, tag=urllib.quote(TagName))
        try:
            print Tagurl
            request = urllib2.Request(Tagurl, headers=headers)
            response = urllib2.urlopen(request)
            tagsoup = BeautifulSoup(response, "lxml")
        except Exception, e:
            print ("    maybe blocked! or the tag:%s don't has so many movies" % (TagName))
            continue

        for items in tagsoup.find_all('a', {'class': 'nbg'}):
            filmurllist = re.findall(r'<a class="nbg" href="(.*?)" title="(.*?)">', str(items))
            for FilmUrl in filmurllist:
                print FilmUrl[0]

                if GetComments(FilmUrl, TagName) == False:
                    continue
    return True


def GetComments(Film, TagName):
    '''
    :param urlComments: movie'url in pangeNumber in movie type and movie id
    :return:
    '''
    global movieName2ID,movieID, useName2ID, userID
    commentcomplete = []
    urlComments, movieName = Film

    #获取movieID_
    if not (movieName2ID.has_key(movieName)):
        movieID = movieID + 1
        movieName2ID.update({movieName: movieID})
        movieID_ = movieID
    else:
        return False

    headers = BrowserHeaders()
    nextpage = "comments?start={commentNum}&limit=20&sort=new_score"

    #爬取10页评论
    for commentPages in range(1):
        begin_page = time.time()
        # time.sleep(2)
        pageNum = commentPages * 20
        SingleCommentsPage = nextpage.format(commentNum=pageNum)

        try:
            request = urllib2.Request(urlComments + SingleCommentsPage, headers=headers)
            print urlComments + SingleCommentsPage
            response = urllib2.urlopen(request)
            commentSoup = BeautifulSoup(response, "lxml")
        except Exception, e:
            print ("        maybe blocked or the movie: %s don't has so many comments!" % (movieName))
            return False

        #获取每页的所有评论
        for commentsDetail in commentSoup.find_all('div', {'class': 'comment'}):
            # get rate
            rate = re.search(r'<span class="allstar(.*?) rating" title=".*?"></span>.*?', str(commentsDetail))
            if rate != None:
                rate = rate.group(1)

            #获取每条评论的userID_
            userName = re.search(r'<a class=.*?href="https.*?">(.*?)</a>.*?', str(commentsDetail))
            if userName != None:
                userName = userName.group(1)
            if not (useName2ID.has_key(userName)):
                userID = userID + 1
                useName2ID.update({userName: userID})
                userID_ = userID
            else:
                userID_ = useName2ID[userName]

            #将movieID_, movieName, userID_, userName, rate, TagName写入csv
            item = [movieID_, movieName, userID_, userName, rate, TagName]
            commentcomplete.append(item)
            Writecsv(commentcomplete)
            commentcomplete.pop()

        end_page = time.time()
        print ("        crawling comment page%d in movie: %d %s userID: %d , and time is %f..." % (
        commentPages + 1, movieID_, movieName, userID_, end_page - begin_page))



def Writecsv(commentcomplete):
    with open('smallcomment.csv', 'ab+') as csvfile:
        writer = csv.writer(csvfile)
        for singlecomment in commentcomplete:
            writer.writerow(singlecomment)
    csvfile.close()


global movieID, useName2ID,movieName2ID, userID
useName2ID = {}
movieName2ID = {}
movieID = 0
userID = 0
GetTag()

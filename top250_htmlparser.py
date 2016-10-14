# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 13:34:46 2016

@author: neeziv
"""
import urllib.request
from html.parser import HTMLParser
import csv


url = 'http://www.imdb.com/chart/top'

sourcePage = urllib.request.urlopen(url).read().decode('utf-8')

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.lastAttr    = None
        self.lasttag = None
        self.inLink = False
        self.titles = []
        self.lastTitle = ''
        
    def handle_starttag(self, tag, attrs):
        self.inLink = False
        global count #using to mark rank - first occurence will be count/rank1 last occurence will be count/rank250
        self.lasttag = tag
        if tag == 'td':
            for name,value in attrs:
                if name =='class' and value=='titleColumn':
                    count +=1
                    self.lastAttr = value
                elif name=='class' and value =='ratingColumn imdbRating':
                    self.lastAttr = value
        elif (tag == 'a' or tag == 'strong')and (self.lastAttr =='titleColumn' or self.lastAttr =='ratingColumn imdbRating'):
            self.inLink = True
        else:
            self.lastAttr =None
 
            
    def handle_data(self, data):
        if self.inLink and data.strip() and self.lastAttr=='titleColumn':
            self.lastTitle = data
        if self.inLink and data.strip() and self.lastAttr =='ratingColumn imdbRating':
            self.titles.append([count,self.lastTitle, data])
        
        
count =0
parser = MyHTMLParser()
parser.feed(sourcePage)


with open('mycsvfile.csv','w') as f:
    w = csv.writer(f)
    w.writerows(parser.titles)



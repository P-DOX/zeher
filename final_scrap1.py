import time
import json 
from hashlib import sha256
from datetime import datetime
from bingsearch import bsearch
from googlesearch import gsearch
from newsplease import NewsPlease 
from urllib.error import HTTPError
from random import randint,shuffle,choice
import os

fileName = "/home/ubuntu/zeher/articles/pep_4.json"
# fileName = "list.json"
class ContentError(Exception):
   """Base class for other exceptions"""
   #For avoiding null/None type content 
   pass

count = 1
def savelog(article):
    global count
    with open("data_"+str(count)+".json",'w',encoding= 'utf8') as json_file:
        json.dump(article , json_file , ensure_ascii = False)

    count = count +1
	# with open("log.txt",'a')as f:
	# 	f.write(log)

def getSource(url):
	lst = url.split('/')
	return lst[2]

def date_to_string(pub_date):
	# print(pub_date)		#"2020-04-27T23:00:09Z
	try:
		pub_date = str(pub_date)
		date,time = pub_date.split(" ")
		dateTime = str(date)+"T"+str(time)
		return dateTime
	except:
		return str(pub_date)

def fetchInfo(url,name,list_type):
    info = {'title' : '' , 'source' : '' ,'description':'', 'publishedAt' :'' ,'link':url , 'query':name ,'uid':-1,'content':'' , 'list_type':list_type}
    try:
        article = NewsPlease.from_url(url,timeout=10)
        info['title'] = article.title
        info['publishedAt'] = date_to_string(article.date_publish)
        info['description'] = article.description
        info['content'] = article.maintext
        info['source'] = getSource(url)
        info['uid'] = int.from_bytes(sha256(url.encode('utf-8')).digest(), 'big')

		# info = {'title' : title , 'source' : source ,'description':description, 'publishedAt' :publishedAt ,'link':url , 'query':word ,'uid':uid,'content':content , 'list_type':"sdn"}

        if(len(info['content']) < 250):
        	raise ContentError

    except ContentError:
    	return [False , info]
    except : 
        return [False , info]

    return [True , info]


def updatePerson(person):
	global fileName
	with open(fileName,'w',encoding= 'utf8') as json_file:
		json.dump(person , json_file , ensure_ascii = False)

def readPerson():
    global fileName
    with open(fileName, 'rb') as f:
        person = json.load(f)

    return person



def main():
    person = readPerson()
    for name in  person:
        y=choice([1,2])
        if y==1:
        	x=gsearch(name+" news",num=15)
        elif y==2:
        	x=bsearch(name+" news",num=15)

        time.sleep(randint(30,60))

        for url in x:
            try:
                info = fetchInfo(url,name,'pep')
                if info[0] :
                    article = {"article":[info[1]]}
                    article = json.dumps(article)
                    print(article)
                    # print(url,name)
                    # savelog(article)
            except:
            	pass
        # del person[name]
        person.remove(name)         
        updatePerson(person)



if __name__ == "__main__": 
	main()

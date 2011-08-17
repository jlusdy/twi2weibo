#coding=utf-8
from weibopy.auth import OAuthHandler
from weibopy.api import API

import time
import urllib,sys,socket
import simplejson as json

socket.setdefaulttimeout(5)

consumer_key= 'yyy'
consumer_secret ='yyy'
token = 'xxx'
tokenSecret = 'xxx'

t_timeline_url = 'https://twitter.com/statuses/user_timeline/yyy.json'
twitter_last_id = '0'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.setToken(token, tokenSecret)
api = API(auth)

while 1:
    try:
        tl_file = urllib.urlopen(t_timeline_url)
        timeline = json.load(tl_file)
        if twitter_last_id == '0':
            twitter_last_id = timeline[0]['id_str']
            print 'init twitter_id:'
            print twitter_last_id
        if isinstance(timeline,list):
            tweets_to_be_post = []
            for tl in reversed(timeline):
                if long(tl['id_str']) > long(twitter_last_id):
                    tweets_to_be_post.append({'id_str':tl['id_str'],'text':tl['text']})
            if len(tweets_to_be_post) > 0:
                for tweet_obj in tweets_to_be_post:
                    cur_id = tweet_obj['id_str']
                    cur_tweet = tweet_obj['text']
                    twitter_last_id = cur_id
                    print twitter_last_id
                    if cur_tweet.startswith('@'):
                        continue
                    if cur_tweet.count('http://t.co') > 0:
                        for segment in cur_tweet.split():
                            if segment.startswith('http://t.co'):
                                realresponse = urllib.urlopen(segment)
                                if realresponse.getcode() == 200:
                                    cur_tweet = cur_tweet.replace(segment,realresponse.geturl())
                    api.update_status(cur_tweet)
    except Exception as tui2lang:
        print time.ctime()
        print tui2lang
    time.sleep(90)

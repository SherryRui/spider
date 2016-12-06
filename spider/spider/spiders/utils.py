#!/user/bin/env python
#encoding:utf-8
import requests
import os
import re
import urllib2
import logging
import json

header = {}
header['Accept'] = 'application/json'
header['Accept-Encoding'] = 'gzip, deflate, sdch, br'

def conn_try_again(function):
    RETRIES = 0
    #重试的次数
    count = {"num": RETRIES}
    def wrapped(*args, **kwargs):
      try:
        return function(*args, **kwargs)
      except Exception, err:
        if count['num'] < 2:
          count['num'] += 1
          return wrapped(*args, **kwargs)
        else:
          raise Exception(err)
    return wrapped

     
#@conn_try_again
def http_request(method, url, data = {}, header = header):
    try:
        if method == 'GET':
            r = requests.get(url, data = data, headers = header)
            return r
        elif method == 'POST':
            r = requests.post(url, data = data, headers = header)
            return r
        else:
            return None
    except Exception as e:
        logging.exception('[http error] http request connection error %s'% e)


def get_urls_list(response):
    '''
		获取要爬取的url列表
    '''
    urls = []
    raw_data = response.text
    datas = json.loads(raw_data)
    for d in datas['data']:
        url = d['article_url']
        urls.append(url)
    return urls


def save_img2disk(path, img_url):  
    '''
        根据图片的地址，下载图片并保存在本地   
    '''
    f = open(path +'/'+ img_url[-7:] +'.jpg','wb')  
    req = urllib2.urlopen(img_url)  
    buf = req.read()  
    f.write(buf)
    logging.info('Image %s has been saved .' % (path + img_url))

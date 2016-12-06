#!/user/bin/env python
#encoding:utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
#from tutorial.items import 
from utils import http_request, get_urls_list, save_img2disk
import requests
import os
import re
import urllib2
import json
import logging

class ToutiaoSpider(BaseSpider):
    name = "toutiao"
    allowed_domains = ["toutiao.com"]
    start_urls = []    
    url = 'http://www.toutiao.com/search_content/?offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&_=1481020204161'
    method = 'GET'
    r = http_request(method, url)
    if r and r.status_code == requests.codes.ok:
        start_urls = get_urls_list(r)
    print start_urls


    def parse(self, response):
        selector = Selector(response)
        title = selector.xpath('//*[@id="article-main"]/h1/text()').extract()
        sub_dir = ''
        if title:
           sub_dir = title[0]
        else:
           sub_dir = 'default'
        img_urls = selector.xpath('//p/img/@src').extract()
        path = os.getcwd() + '/download_images/' + sub_dir
        if not os.path.exists(path):
            os.makedirs(path)
        for img_url in img_urls:
            save_img2disk(path, img_url)

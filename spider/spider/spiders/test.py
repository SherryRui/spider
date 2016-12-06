#!/user/bin/env python
#encoding:utf-8
import requests
from cookielib import LWPCookieJar
import os
import re
import urllib
import json

'''
常量值
'''
user = ''
password = ''
header = {}
header['Accept'] = 'application/json'
header['Accept-Encoding'] = 'gzip, deflate, sdch, br'

#http连接有问题时候，自动重连
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
 
@conn_try_again
def http_request(session, method, url, data = {}, header = header):
    try:
        if method == 'GET':
            r = session.get(url, data = data, headers = header)
            return r
        elif method == 'POST':
            r = session.post(url, data = data, headers = header)
            return r
        else:
            return None
    except Exception as e:
        logging.exception('[online_statistics] http request connection error %s'% e)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    s = requests.Session()
    s.cookies = LWPCookieJar('cookiejar')
    user = base64.decodestring(user)
    pwd = base64.decodestring(password)
    #payload = {'username':user,'password':pwd}
    if not os.path.exists('cookiejar'):
        r = http_request(s, 'POST', login_url, payload, header)
        s.cookies.save(ignore_discard=True)
    else:
        s.cookies.load(ignore_discard=True)
    record = []
    counter = 0
    query_str = 'status:' + status + ' project:' + project + ' after:"' + after + '"'
    url = request_url + urllib.quote_plus(query_str, ':') + '&O=81'
    r = http_request(s, 'GET', url, payload, header)
    if r.status_code == requests.codes.ok:
        raw =  r.text.replace(r")]}'",'',1)
        counter, record = pack_record_info(raw) 

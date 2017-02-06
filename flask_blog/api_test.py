#!/usr/bin/python
#-*- coding:utf-8 -*-

from urllib import urlencode
import urllib2
from xml.etree.ElementTree import parse
def query(query_name):
    params = {'query': query_name.encode('utf8') }
    params = urlencode(params)
    req = urllib2.Request('https://openapi.naver.com/v1/search/encyc.xml?'+params)
    req.add_header('Referer', 'http://http://52.78.55.223/')
    req.add_header('Host', 'openapi.naver.com')
    req.add_header('User-Agent', 'curl/7.43.0')
    req.add_header('Accept', '*/*')
    req.add_header('Content-Type', 'application/xml ')
    req.add_header('X-Naver-Client-Id', 'hyW7dhq1KZmI4IMvKxnw')
    req.add_header('X-Naver-Client-Secret', 'ouSg2Aj6mJ')
    r = urllib2.urlopen(req)
    return r

def get(q_result):
    with open('tmp.xml','w' ) as fp:
        fp.write(q_result)
    tree = parse('tmp.xml')
    root = tree.getroot()
    for item in root.iter('title'):
        print item.text

if __name__ == '__main__':
    q_result = query(u'기름칠래라라라').read()
    get(q_result)

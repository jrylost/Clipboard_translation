# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 11:15:27 2019

@author: Administrator
"""

import win32clipboard as w
from win32con import CF_UNICODETEXT as cons
from time import sleep
from re import sub
import json

import requests
import time
import random
import hashlib,re

class clipstr(object):
    def __init__(self):
        self.textdata=self.getclipdata() 
        self.modifydata=self.textdata
        
    def getclipdata(self):
        w.OpenClipboard()
        try:
            t=w.GetClipboardData(cons)
        except:
            t='Please don\'t choose files or other objects.'
        finally:
            w.CloseClipboard()
        return t
    
    def modifyclipdata(self):
        self.modifydata=sub(r"[\r\n]", " ", self.modifydata)
        
    def writeclipdata(self):
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(cons,self.modifydata)    
        w.CloseClipboard()


class translation(object):
    def __init__(self,origin_text=''):
        self.s = requests.session()
        r = str(int(time.time()*1000))
        i = r + str( random.randint(0,10))
        t = origin_text
        lent=t.__len__()
        u = 'fanyideskweb'
        l = str(self.getjs())
        src = u + t + i + l
        m2 = hashlib.md5()
        m2.update(src)
        str_sent = m2.hexdigest()
        src='5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        m2.update(src)
        str_sent2 = m2.hexdigest()
        head = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Content-Length':str(lent+254),
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'fanyi.youdao.com',
            'Origin':'http://fanyi.youdao.com',
            'Referer':'http://fanyi.youdao.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
        }
        head['Cookie'] = 'OUTFOX_SEARCH_USER_ID=1112068406@10.169.0.84; JSESSIONID=aaa4R-90JCAGCeDTxwPKw; OUTFOX_SEARCH_USER_ID_NCOO=349562757.7712379; SESSION_FROM_COOKIE=www.cnblogs.com;___rl__test__cookies='+i        
        data = {
            'i': t,
            'from':'AUTO',
            'to':'AUTO',
            'smartresult':'dict',
            'client':'fanyideskweb',
            'salt':i,
            'sign':str_sent,
            'ts':r,
            'bv':str_sent2,
            'doctype':'json',
            'version':'2.1',
            'keyfrom':'fanyi.web',
            'action':'FY_BY_CLICKBUTTON',
            'typoResult':'false'
        }
        url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        p = self.s.post(url,data= data,headers = head)
        self.transresult= p.text

    def getjs(self):
        url = 'http://fanyi.youdao.com'
        try:
            p=self.s.get(url)
            serobj =re.compile(r'src=.+fanyi.min.js').findall(p.text)
            qqq=self.s.get(serobj[0][5:])
            serobj2 =re.compile(r'sign:n.md5\(\"fanyideskweb\".{27}').findall(qqq.text)
            return serobj2[0][-21:]
        except:
            return 'p09@Bn{h02_BIEe]$P^nG'

print u'''
    pdf拷贝自动删除换行并从有道爬取翻译。
    Designed by Jerry Jiang
    gisk94@163.com
    https://github.com/jrylost/clipboard_translation
    '''        
u=clipstr()
while 1:
    sleep(0.2)
    st=clipstr()
    if u.textdata==st.textdata:
        continue
    else:
        st.modifyclipdata()
        content=st.modifydata.encode('utf-8')
        html=translation(content).transresult
        target=json.loads(html)
        st.modifydata=content.decode('utf-8')+'\n'+''.join([x['tgt'] for x in target['translateResult'][0]])
        st.writeclipdata()
        try:
            st.modifydata.encode('gbk'),'\n'
            print st.modifydata
        except:
            print u'原文含有非法字符,控制台无法显示。\n'
            print ''.join([x['tgt'] for x in target['translateResult'][0]])
        finally:
            st.textdata=st.modifydata
            u.textdata=st.textdata
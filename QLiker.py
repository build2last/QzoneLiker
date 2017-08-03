# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import random
import json
import os
import sys
import datetime
import time
import threading
import logging
import execjs
import urllib
from HttpClient import HttpClient

reload(sys)
sys.setdefaultencoding("utf-8")

# CONFIGURATION FIELD
checkFrequency = 180
#check every k seconds
# STOP EDITING HERE
HttpClient_Ist = HttpClient()
UIN = 0
skey = ''
Referer = 'https://user.qzone.qq.com/'
QzoneLoginUrl = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=https%3A//qzs.qq.com/qzone/v6/portal/proxy.html&daid=5&&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=22&target=self&s_url=https%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&pt_qr_app=%E6%89%8B%E6%9C%BAQQ%E7%A9%BA%E9%97%B4&pt_qr_link=https%3A//z.qzone.com/download.html&self_regurl=https%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=https%3A//z.qzone.com/download.html&pt_no_auth=0'

initTime = time.time()


logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')

def getAbstime():
    return int(time.time())
    
def date_to_millis(d):
    return int(time.mktime(d.timetuple())) * 1000

def getReValue(html, rex, er, ex):
    v = re.search(rex, html)

    if v is None:
        logging.error(er)

        if ex:
            raise Exception, er
        return ''

    return v.group(1)

def getQRtoken(qrsig):
    e = 0
    for i in qrsig:
        e += (e << 5) + ord(i)
    return 2147483647 & e;
    
# -----------------
# 登陆
# -----------------
class Login(HttpClient):
    MaxTryTime = 5

    def __init__(self, vpath, qq=0):
        global UIN, Referer, skey
        self.VPath = vpath  # QRCode保存路径
        AdminQQ = int(qq)
        logging.critical("正在获取登陆页面")
        self.setCookie('_qz_referrer','qzone.qq.com','qq.com')
        self.Get(QzoneLoginUrl,'https://qzone.qq.com/')
        StarTime = date_to_millis(datetime.datetime.utcnow())
        T = 0
        while True:
            T = T + 1

            self.Download('https://ssl.ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=3&d=72&v=4&t=0.{0}6252926{1}2285{2}86&daid=5'.format(random.randint(0,9),random.randint(0,9),random.randint(0,9)), self.VPath)
            LoginSig = self.getCookie('pt_login_sig')
            QRSig = self.getCookie('qrsig')
            logging.info('[{0}] Get QRCode Picture Success.'.format(T))           
            while True:
                html = self.Get('https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&ptqrtoken={0}&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-{1}&js_ver=10220&js_type=1&login_sig={2}&pt_uistyle=40&aid=549000912&daid=5&'.format(getQRtoken(QRSig),date_to_millis(datetime.datetime.utcnow()) - StarTime, LoginSig), QzoneLoginUrl)
                # logging.info(html)
                ret = html.split("'")
                if ret[1] == '65' or ret[1] == '0':  # 65: QRCode 失效, 0: 验证成功, 66: 未失效, 67: 验证中
                    break
                time.sleep(2)
            if ret[1] == '0' or T > self.MaxTryTime:
                break

        if ret[1] != '0':
            raise ValueError, "RetCode = "+ret[1]
            return
        logging.critical("二维码已扫描，正在登陆")
        
        # 删除QRCode文件
        if os.path.exists(self.VPath):
            os.remove(self.VPath)

        # 记录登陆账号的昵称
        tmpUserName = ret[11]

        self.Get(ret[5])
        UIN = getReValue(ret[5], r'uin=([0-9]+?)&', 'Fail to get QQ number', 1)
        Referer = Referer+str(UIN)
        skey = self.getCookie('p_skey')
        logging.critical("Successfully Login, Username: "+str(tmpUserName))

# -----------------
# 计算g_tk
# -----------------  
def utf8_unicode(c):            
    if len(c)==1:                                 
        return ord(c)
    elif len(c)==2:
        n = (ord(c[0]) & 0x3f) << 6              
        n += ord(c[1]) & 0x3f              
        return n        
    elif len(c)==3:
        n = (ord(c[0]) & 0x1f) << 12
        n += (ord(c[1]) & 0x3f) << 6
        n += ord(c[2]) & 0x3f
        return n
    else:                
        n = (ord(c[0]) & 0x0f) << 18
        n += (ord(c[1]) & 0x3f) << 12
        n += (ord(c[2]) & 0x3f) << 6
        n += ord(c[3]) & 0x3f
        return n

def getGTK(skey):
    hash = 5381
    for i in range(0,len(skey)):
        hash += (hash << 5) + utf8_unicode(skey[i])
    return hash & 0x7fffffff
# -----------------
# LIKE
# ----------------- 
def like(unikey,curkey,dataid,time,qztoken):
    reqURL = 'https://h5.qzone.qq.com/proxy/domain/w.qzone.qq.com/cgi-bin/likes/internal_dolike_app?g_tk={0}&qzonetoken={1}'.format(str(getGTK(skey)),str(qztoken))
    data = (
            ('qzreferrer', Referer),
            ('opuin', UIN),
            ('unikey', str(unikey)),
            ('curkey', str(curkey)),
            ('from', '1'),
            ('appid', '311'),
            ('typeid', '0'),
            ('abstime', str(time)),
            ('fid', str(dataid)),
            ('active', '0'),
            ('fupdate', '1')
        )
    rsp = HttpClient_Ist.Post(reqURL, data, Referer)
    getReValue(rsp, r'"code":(0)', 'Fail to like unikey='+str(unikey)+';curkey='+str(curkey)+';fid='+str(dataid), 0)

# -----------------
# 主函数
# ----------------- 
def MsgHandler():
    html=HttpClient_Ist.Get(Referer+'/infocenter?via=toolbar',Referer)
    fkey=re.findall(r'<div class="f-item f-s-i" id=".*?" data-feedsflag=".*?" data-iswupfeed=".*?" data-key="(.*?)" data-specialtype=".*?" data-extend-info=".*?"',html)
    if not fkey:
        raise Exception, 'Fail to find any feeds'
    g_qzonetoken=re.search(r'window\.g_qzonetoken = \(function\(\)\{ try\{return (.*?);\} catch\(e\)',html)
    g_qzonetoken=g_qzonetoken.group(1)
    ctx = execjs.compile('function qz(){location = "./"; return '+g_qzonetoken+'}')
    qztoken=str(ctx.call("qz"))
    split_string=re.split(r'<div class="f-item f-s-i" id=".*?" data-feedsflag=".*?" data-iswupfeed=".*?" data-key=".*?" data-specialtype=".*?" data-extend-info=".*?"',html)
    for i in range (0,len(fkey)):
        try:
            btn_string = re.search(r'<a class="item qz_like_btn_v3.*?" data-islike="0" data-likecnt=".*?" data-showcount=".*?" data-unikey="(.*?)" data-curkey="(.*?)" data-clicklog="like" href="javascript:;">', split_string[i+1])
            if btn_string is None:
                continue
            abstime = re.search(r'data-abstime="(\d*?)"',split_string[i+1])
            if abstime is None:
                continue
            like(btn_string.group(1),btn_string.group(2),fkey[i],abstime.group(1),qztoken)
            logging.info('已点赞'+btn_string.group(2))
        except Exception, e:
            logging.error(str(e))

def exe(QQLIST=[]):
    import conf
    vpath = conf.QRCode_PATH
    qq = 0
    try:
        qqLogin = Login(vpath, qq)
    except Exception, e:
        logging.critical(str(e))
        os._exit(1)
    errtime=0
    while True:
        try:
            if errtime > 5:
                break
            MsgHandler()
            if UIN not in QQLIST:
                QQLIST.append(UIN)
            time.sleep(checkFrequency)
            errtime = 0
        except Exception, e:
            logging.error(str(e))
            errtime = errtime + 1
    if UIN in QQLIST:
        QQLIST.remove(UIN)

# -----------------
# 主程序
# -----------------

if __name__ == "__main__":
    image_dir = "image"
    if not os.path.exists(image_dir):
        os.makedir(image_dir)
    vpath = os.path.join(image_dir, 'v.png')
    qq = 0
    if len(sys.argv) > 1:
        vpath = sys.argv[1]
    if len(sys.argv) > 2:
        qq = sys.argv[2]

    try:
        qqLogin = Login(vpath, qq)
    except Exception, e:
        logging.critical(str(e))
        os._exit(1)
    errtime=0
    while True:
        try:
            if errtime > 5:
                break
            MsgHandler()
            time.sleep(checkFrequency)
            errtime = 0
        except Exception, e:
            logging.error(str(e))
            errtime = errtime + 1

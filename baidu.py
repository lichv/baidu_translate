#!/usr/bin/python
# -*- coding: UTF-8 -*-

import execjs
import requests
import json
import os

class Baidu(object):

    #基础URL
    baseURL = "https://fanyi.baidu.com"
    baiduID = ""
    gtk = ""
    token = ""


    """docstring for Baidu"""
    def __init__(self):
        super(Baidu, self).__init__()
        self.initData()

    """
    获取配置
    """
    def initData(self):
        filepath = os.path.join( os.getcwd(),"./token.ini" )
        if os.path.exists( filepath ):
            with open(filepath,'r',encoding="utf-8") as f:
                self.token = f.readline()[0:-1]
                self.gtk = f.readline()[0:-1]
                self.baiduID = f.readline()[0:-1]
        else:
            self.token,self.gtk,self.baiduID = self.getToken()
            with open(filepath,'w',encoding="utf-8") as f:
                f.write(token+'\n')
                f.write(gtk+'\n')
                f.write(baiduID+'\n')

    """
    获取token.gtk,baiduID
    """
    def getToken(self):
        baiduID = ""
        headers = {
            'dnt': "1",
            'origin': 'https://fanyi.baidu.com',
            'referer': 'https://fanyi.baidu.com/',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'cache-control': 'no-cache',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
        }
        res = requests.get(self.baseURL,headers=headers)
        res.encoding='utf-8'
        html = res.text

        token = res.text.split('systime')[0][-39:-7]
        gtk = html.split('window.gtk')[1][4:20]
        cookies = requests.utils.dict_from_cookiejar(res.cookies)
        if cookies['BAIDUID']:
            baiduID = cookies['BAIDUID']
        return token,gtk,baiduID
    """
    取账户余额
    """
    def translate(self,word):
        url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'
        cookie = self.getCookie(self.baiduID)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
            "cookie":cookie
        }

        data = {
            "from":"en",
            "to":"zh",
            "query":word,
            "transtype": "realtime",
            "simple_means_flag":3,
            "sign":self.sign(word,self.gtk),
            "token":self.token,
            "domain":"common",
        }
        response = requests.post(url, headers=headers, data=data).json()
        return response

    """
    获取cookie
    """
    def getCookie(self, baiduID):
        cookies = {
          'Hm_lvt_64ecd82404c51e03dc91cb9e8c025574': '1576827811',
          'Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574': '1576831062',
          'from_lang_often': '%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D',
          'REALTIME_TRANS_SWITCH': 1,
          'FANYI_WORD_SWITCH': 1,
          'HISTORY_SWITCH': 1,
          'SOUND_SPD_SWITCH': 1,
          'SOUND_PREFER_SWITCH': 1,
          'to_lang_often': '%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D',
          'APPGUIDE_8_2_2': 1,
          '__yjsv5_shitong': '1.0_7_76a54445e702784530b76123583169a790f1_300_1576831062115_27.10.55.214_f1f1fe71',
          'BIDUPSID': 'C62D680D801B9AAA1F7B34FFB0EB9A2A',
          'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
          'X-Requested-With': 'XMLHttpRequest',
        }
        cookies['BAIDUID'] = baiduID
        result = ""
        for k in cookies:
            result +=k+"="+str(cookies[k])+";"
        return result

    """
    签名
    """
    def sign(self, query, gtk):
        result = ""
        with open('./baidu_translate_sign.js', 'r', encoding='utf-8') as f:
            ctx = execjs.compile(f.read())
            result = ctx.call('e', query, gtk)
        return result


if __name__ == "__main__":
    service = Baidu()
    result = service.translate("translate")
    print(result)


# encoding: utf-8
from bs4 import BeautifulSoup
from urllib2 import urlopen
import numpy as np
import cv2
import urlparse
import validators
import requests
import re
import json
import data_manager
import constant

class HtmlParser(object):
    """docstring for HtmlParser"""
    def __init__(self):
        super(HtmlParser, self).__init__()
    

    #爬取所有页面地址，第几页
    def parse_all_pages(self,web_data,root_url):
        page_urls = set()
        soup = BeautifulSoup(web_data,"html.parser")
        pageElement = soup.find('div', attrs={'id':'page'}, recursive=True, text=None, kwargs='')
        page_A_elements = pageElement.findAll('a')

        for a in page_A_elements:
            url_suffix = a['href']
            whole_url = urlparse.urljoin(root_url,url_suffix)
            if validators.url(whole_url):
                page_urls.add(whole_url)

        return page_urls

    #爬取的每一个商品房的地址 #http://www.cdgzc.com/gongshigonggao/201807/1067.html
    def parser_data(self,web_data,root_url):
        
        new_urls = []
        soup = BeautifulSoup(web_data,"html.parser")
        ul = soup.find('ul', attrs={'class':'gsgg-list'}, recursive=True, text=None, kwargs='')
        lis = ul.findAll('li')

        for ams in lis:
            a_more = ams.find('a', attrs={'class':'more'})
            link_suffix = a_more['href']
            date_p = ams.find('p', attrs={'class':'date-box'})
            whole_url_path = urlparse.urljoin(root_url,link_suffix)
            date_content = date_p.get_text()
            # #对比时间，获取最新的下载链接
            last_craw_data = data_manager.datamanager.find_data_link_lastnew()
            if last_craw_data:
                last_time_content = last_craw_data.get('publishDate')
                print('leanData',last_time_content)
                print('time',last_time_content)
                #没有最新的资料
                if  last_time_content >= date_content:
                    return None;

            if validators.url(whole_url_path):
                userful_data = {"url":whole_url_path,"date":date_content}
                new_urls.append(userful_data)

        return new_urls


    def parser_excel_data(self,web_data,root_url):
        
        new_urls = []
        soup = BeautifulSoup(web_data,"html.parser")
        dataExcelElements = soup.findAll('p')

        for link in dataExcelElements:
            spanElements = link.findAll('span')
            for span in spanElements:
                if span.get_text() == 'xls':
                    a_element = link.find('a')
                    yunPanLink = a_element['href']
                    title = a_element.get_text()
                    if validators.url(yunPanLink):
                        link_dic = {constant.KBuilding_title:title,constant.KBuilding_Yun_URL:yunPanLink}
                        new_urls.append(link_dic)
                    break;

        return new_urls

    def get_sign(self,document_url):
        headers = {'Host': 'pan.baidu.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'ChMozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) rome/67.0.3396.99 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': document_url,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': 'FP_UID=2cbcb8a328f50548a27a5ab0e00bbe12; FP_LASTTIME=1500282497726; panlogin_animate_showed=1; pan_login_way=1; PANWEB=1; secu=1; SCRC=4a430b61c3bb39d4119822704eae8990; STOKEN=c96a435704df3470d89eae46641aa0f4df9fe28d1e8591576e77176624c7b665; BAIDUID=A6B1BA0D2E735A76CD0DC872125642D9:FG=1; PSTM=1531101783; BIDUPSID=BD3BE2A81155354871BBFAC154286EE0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; PANPSC=9515220372056209026%3Au2C8FyuEb6hm%2B%2BCLt1X2KUPUkmyfU9eLntQVO6kZ6EXxTJ3v1z1m%2Bo4js0LQbwAgM8d2kZaP94%2F%2Bp%2F8n1715daq6%2F5SRjTJqgs6%2BSP%2BysvgMAXNwiGk043j7YdpwIDfJOy6S0zDqC6VtUVw2SfQVPlW%2BZIpiYpGEpBG7CHFW%2FfQ%3D; H_PS_PSSID=1462_21095_22159; PSINO=3; BCLID=10064227838435095525; BDSFRCVID=id_sJeC626l-GOn7O5twudjle0mXcNvTH6aoeg0QLw0iTKxsYag_EG0PqM8g0KubLu7UogKKXgOTHw3P; H_BDCLCKID_SF=tJAj_DP2fII3DR5mbtQ5bDCthHRqa6veWDTm_D_KaT6n8nu6XToMhbLOMxv-JPrvK2oq-pPKKR7qeIJhXbt2Mq0U2hbk54bd3mkjbPjzfn02OP5PXb_b3t4syPRvKMRnWTkebIF-tKt-bK-9ejR_bJ08-qb-etcLfK5bM-OF5l8-hCQ1qfJch6-gjqOf-43BaIIjWxnJBtQxOKQphPoJDh_T5N30LUnO-a5K0M7N3KJmqqC9bT3v5tDT5HJP2-biWabM2MbdbKOmbRO4-TFKj5c-jxK; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1529571248,1529650704,1531107410,1531201825; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1531201825; Hm_lvt_e6c5e9705447b840241ebab6dbdb5fda=1531122035,1531201837; Hm_lpvt_e6c5e9705447b840241ebab6dbdb5fda=1531201837'
        }
        response = requests.get(document_url, headers=headers)
        # print('response:',response.text)
        #获取下载需要的相关参数
        pattern_result = re.search(r'"sign":"(.*?)"',response.text)
        time_stamp_result = re.search(r'"timestamp":(.+?),',response.text)
        uk_result = re.search(r'"uk":(.+?),',response.text)
        primaryid_result = re.search(r'"shareid":(.+?),',response.text)
        fid_list_result = re.search(r'"fs_id":(.+?),',response.text)
        bdstoken_result = re.search(r'"bdstoken":"(.*?)"',response.text)

        sign = pattern_result.group(1)
        timestamp =  time_stamp_result.group(1)
        uk = uk_result.group(1)
        shareid = primaryid_result.group(1)
        fid_list = fid_list_result.group(1)
        bdstoken = ""
        if bdstoken_result:
            bdstoken = bdstoken_result.group(1)

        # print("sign:",pattern_result.group(1))
        return  sign,timestamp,uk,shareid,fid_list,bdstoken

# "https://pan.baidu.com/api/sharedownload?
# sign=61a4ecc58cd61a15b4d94fb1ff8270a9d1c767df
# &timestamp=1531274502
# &channel=chunlei
# &web=1
# &app_id=250528
# &bdstoken=null
# &logid=MTUzMTI3NDUyMjI2MDAuNDEyNjYyODI4MTMwNzcyNQ==
# &clienttype=0""

# 参数
# encrypt=0
# &product=share
# &uk=990467389
# &primaryid=1114155820
# &fid_list=%5B1012687191473041%5D
# &path_list=
    def get_download_url(self,document_url,sign,timestamp,uk,shareid,fid_list,bdstoken,vcode_input="",vcode_str=""):
        header = {
        'Host': 'pan.baidu.com',
        'Connection': 'keep-alive',
        'Content-Length': '99',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://pan.baidu.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Content-Type': document_url,
        'Referer': 'https://pan.baidu.com/s/1tNpl9fWNqH4OnVjZyT9FjQ?adapt=pc&fr=ftw',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': 'FP_UID=2cbcb8a328f50548a27a5ab0e00bbe12; FP_LASTTIME=1500282497726; panlogin_animate_showed=1; pan_login_way=1; PANWEB=1; secu=1; SCRC=4a430b61c3bb39d4119822704eae8990; STOKEN=c96a435704df3470d89eae46641aa0f4df9fe28d1e8591576e77176624c7b665; BAIDUID=A6B1BA0D2E735A76CD0DC872125642D9:FG=1; PSTM=1531101783; BIDUPSID=BD3BE2A81155354871BBFAC154286EE0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_e6c5e9705447b840241ebab6dbdb5fda=1531122035,1531201837; recommendTime=iphone2018-07-10%2017%3A44%3A27; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1529650704,1531107410,1531201825,1531274503; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1531274503'
        }

        params = {
        "sign":sign,
        "timestamp":timestamp,
        "channel":"chunlei",
        "web":1,
        "app_id":250528,
        "bdstoken":"null",
        "logid":"MTUzMTI5MjQzNzI3NzAuMTI0NDU2MzI3NzE0NjI4MjI=",
        "clienttype":0
        }

        data = {
        "encrypt":0,
        "product":"share",
        "uk":uk,
        "primaryid":shareid,
        "fid_list":json.dumps([fid_list]),
        "path_list":"",
        "vcode_input":vcode_input,
        "vcode_str":vcode_str
        }

        response = requests.post(document_url,headers=header,params=params,data=data)
        # print('response:',response.text)
        # print('header:',response.url)
        dlink_result = re.search(r'"dlink":"(.+?)"',response.text)
        if dlink_result is None:
            # {"errno":-20
            # print('response:',response.text)
            erro_result = re.search(r'"errno":(.+?),',response.text)
            if erro_result:
                erro_num = erro_result.group(1)
                if erro_num == '-20':
                   inputContent,vcode = self.get_vcode(bdstoken)
                   print('inputContent,vcode',inputContent,vcode)
                   return self.get_download_url(document_url,sign,timestamp,uk,shareid,fid_list,bdstoken,inputContent,vcode)
           
        else:
            #下载地址
            dlink = dlink_result.group(1)
            # print('dlinl:',dlink)
            normal_url = dlink.replace("\\","")
            # print('normal_url:',normal_url)

            return normal_url;


# https://pan.baidu.com/api/getvcode?prod=pan
# &t=0.9146544446147236&channel=chunlei
# &web=1&app_id=250528
# &bdstoken=ee3e97251e3a73c4ee0a121d70f35a72
# &logid=MTUzMTM4MDIxOTU1OTAuODY4MzI4MzY1ODk5ODU4OA==
# &clienttype=0
   
    def get_vcode(self,bdstoken):
        header = {
        'Host': 'pan.baidu.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36',
        'Referer': 'https://pan.baidu.com/s/1v7UhoY2BeMtZ3FiLLDoP7w?adapt=pc&fr=ftw',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': 'FP_UID=2cbcb8a328f50548a27a5ab0e00bbe12; FP_LASTTIME=1500282497726; panlogin_animate_showed=1; pan_login_way=1; PANWEB=1; secu=1; BAIDUID=A6B1BA0D2E735A76CD0DC872125642D9:FG=1; PSTM=1531101783; BIDUPSID=BD3BE2A81155354871BBFAC154286EE0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; STOKEN=59b572b1bbfd58f563f890705a32930ad6cde714a0fdedd86c72d847b34d2cb0; SCRC=0af496c83479995c907998b833c60bcd; recommendTime=iphone2018-07-10%2017%3A44%3A27; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1531107410,1531201825,1531274503,1531374312; PSINO=3; H_PS_PSSID=1462_21095_20697_22159; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; Hm_lvt_e6c5e9705447b840241ebab6dbdb5fda=1531122035,1531201837,1531386144; Hm_lpvt_e6c5e9705447b840241ebab6dbdb5fda=1531386144; PANPSC=7204183827816816215%3AiK4yoDyp7LsKy0xVdDWjkiOAoXNFwReXeJnINCW2axMTRUkGLCsQdCz2PhdQts%2FX8Uyd79c9ZvqIibnGfeNoCRyeClXZWmZyfkiVl%2Ff%2FRfwgvcjop0cMIioOm14RA5g23jGzPWbmHcdD1JJsn1PXi57UFTupGehFMngIHoTfOJUWhcYC1XHzFncxjLHpoPTJ; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1531387911'
        }

        params = {
        "prod":"pan",
        "channel":"chunlei",
        "web":1,
        "app_id":250528,
        "bdstoken":"null",
        "logid":"MTUzMTM4Nzk0ODczOTAuMDExMTkzNTk2MjMwNTk3Nzkx",
        "clienttype":0
        }

        vcode_url = "https://pan.baidu.com/api/getvcode"
        response = requests.get(vcode_url, params=params,headers=header)
        print("response",response.text)

        image_address_group = re.search(r'"img":"(.+?)"',response.text)
        vcode_group = re.search(r'"vcode":"(.+?)"',response.text)

        image_address = image_address_group.group(1)
        normal_url = image_address.replace("\\","")
        vcode = vcode_group.group(1)

        print('image_address',normal_url)

        url_response = urlopen(normal_url)
        img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, -1)
        cv2.imshow('URL Image', img)
        cv2.waitKey()

        vcode_content = raw_input('Please Input code:')

        return vcode_content,vcode;


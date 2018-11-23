
# - *- coding: utf- 8 - *-
import url_manager
import html_downloader
import html_parser
import html_outputer
import data_uploader
import data_manager
import constant
import ssl
import local_data_manager
import os
from Fang import fang_main

class SpiderMain(object):
    """docstring for ClassName"""
    def __init__(self):
        super(SpiderMain, self).__init__()
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.uploader = data_uploader.DataUploader()
        self.localDataManager = local_data_manager.LocalDataManager()
        self.pdfDealer = fang_main.PDF_Data_Dealer(self.localDataManager)
    """
    成都公证处
    """
    #爬取所有第几页
    def crow_page(self,rootURL,city):

        page_data = self.downloader.download(rootURL)
        pages_urls = self.parser.parse_all_pages(page_data,rootURL)
        self.urls.append_urls(pages_urls)

        self.crow_detail_data(rootURL,city)


    #网站上数据的链接地址    
    def crow_detail_data(self,rootURL,city):
        
        #网站上的链接地址
        while self.urls.has_url():
            url = self.urls.get_url()
            html_data = self.downloader.download(url)
            data_download_urls = self.parser.parser_data(html_data,rootURL)
            if data_download_urls:
                self.urls.append_detail_urls(data_download_urls)
            else:
                print('没有最新数据！@')
                break

        self.crow_excel_data(rootURL,city)


    def crow_excel_data(self,rootURL,city):
        
        yunpan_datas = []
        while self.urls.has_detail_url():
            dataPath =  self.urls.get_detail_url()
            #链接地址
            url = dataPath["url"]
            data_time = dataPath["date"]
            html_data = self.downloader.download(url)

            data_Save_path = {}
            yunPan_urls = self.parser.parser_excel_data(html_data,rootURL)
            #网盘地址
            data_Save_path[constant.KExcel_Yun_URL] = yunPan_urls
            data_Save_path["date"] = data_time
            data_Save_path["dataURL"] = url
            yunpan_datas.append(data_Save_path)

        #上传到服务器
        for  item in yunpan_datas:
            url = item["dataURL"]
            date = item["date"]
            yun_pan_URL = item["excelYunPanURL"]
            self.uploader.upload_data_save_url(url,city,date,False,rootURL,yun_pan_URL)


    #爬取链接下的地址
    def crow_download_excel_url(self):
        baidu_pan_urls = data_manager.datamanager.find_all_data_not_download()
        if baidu_pan_urls:
           data_property = baidu_pan_urls.pop()
           yunPan_urls = data_property.get(constant.KExcel_Yun_URL)
           print('云盘地址：')
           print(yunPan_urls)
           self.craw_array_excel_url(yunPan_urls,data_property)

    #每一个链接下有多个excel地址
    def craw_array_excel_url(self,array,yunPorperty):
        if array is None or len(array) == 0:
            self.crow_download_excel_url()
            return ;
        yun_pan_url = array.pop()
        if yun_pan_url:
           firstURl = yun_pan_url[constant.KBuilding_Yun_URL] + "?adapt=pc&fr=ftw"
           sign,timestamp,uk,shareid,fid_list,bdstoken = self.parser.get_sign(firstURl)
           donwload_url = self.parser.get_download_url("https://pan.baidu.com/api/sharedownload",sign,timestamp,uk,shareid,fid_list,bdstoken)
           if donwload_url is None:
            #遇到验证码没有解析成功，即停止
            return ;
           else:
             print("excel直接下载地址：")
             print(donwload_url)
             title = yun_pan_url[constant.KBuilding_title]
             self.uploader.update_data_withExcelDownloadURL(yunPorperty,donwload_url,title)
           

        self.craw_array_excel_url(array,yunPorperty)

    #解析Excel摇号排名数据
    def analyze_excel_ranking_data(self):
        property = data_manager.datamanager.find_data_not_analyzied()
        if property:
            excel_address_array = property.get(constant.KExcel_download_URL)
            date = property.get('publishDate')
            #分析Excel数据
            self.analyze_excel_array(excel_address_array,date,property)
        else:
            print("全部分析完毕！")
      

# [{"yunPanURL":"https://pan.baidu.com/s/1xPxs68X51WFloiIYILvncg","bbuildingTitle":"2018年5月14日瀚城新天地4栋刚需登记购房人公证摇号排序结果"},{"yunPanURL":"https://pan.baidu.com/s/1oG9ahybH_yluuID2aru1dA","buildingTitle":"2018年5月14日瀚城新天地4栋棚改货币化安置住户公证摇号排序结果"},{"yunPanURL":"https://pan.baidu.com/s/19CTFm1MdH0Znhwkb61Qtxw",
# "buildingTitle":"2018年5月14日瀚城新天地4栋普通登记购房人公证摇号排序结果"}]
# #解析Excel数组里面每条地址
    def analyze_excel_array(self,array,date,yunPorperty):
       if array is None or len(array) == 0:
        #更改解析状态
        self.uploader.update_data_withExcelAnalyzed(yunPorperty,True)
        #Excel解析完毕，进行下一组递归
        self.analyze_excel_ranking_data()
       else:
        address_dic = array.pop()
        address = address_dic[constant.KBuilding_Yun_URL]
        title = address_dic[constant.KBuilding_title]
        excel_name = title + ".xls"
        print("发布时间：")
        print(date)
        print("下载地址：")
        print(address)
        file_path = os.path.dirname("/Users/kanglin/Python/data/")
        self.downloader.download_file(address,file_path,excel_name)
        data_manager.datamanager.analysis_excel_choseHouseOrder_data(excel_name,self.upload_excel_data,title,date)
        #继续解析excel
        self.analyze_excel_array(array,date,yunPorperty)


    #上传Excel数据到Leancloud
    def upload_excel_data(self,data_array):
        self.uploader.upload_excel_ranking(data_array)


    #重置已获取下载地址标志，方便重新获取下载地址
    def reset_data_notAnalyzed_to_notDownload(self):
        itemsArray = data_manager.datamanager.find_all_data_not_analyzied()
        for item in itemsArray:
            self.uploader.reset_data_not_analyzed_to_not_download(item,False)

    
    """
    成都房协会
    """
    def crow_House_New_Info(self,rootURL,city):

        page_data = self.downloader.download(rootURL)
        pages_urls = self.parser.parse_House_Info(page_data,rootURL)
        print('pageURLS',pages_urls)
        if pages_urls is None:
            return
        lastProperty = data_manager.datamanager.find_Housedata_lastnew()
        for url in pages_urls:
            #def upload_House_Orign_Info(self,houseName,onMarketDate,tel,sourceURL,docoratePlan):
            web_data = self.downloader.download(url)
            title,date,tel,sourceURL,priceURL,pageURL =self.parser.parse_House_Detail(web_data,url)
            if lastProperty:
                last_time_content = lastProperty.get(constant.KDate_Key)
                print('leanData',last_time_content)
                print('time',date)
                #没有最新的资料
                if  last_time_content >= date:
                    print('房协网没有最新数据')
                    break;
            if title is None and date is None:
               break
            self.uploader.upload_House_Orign_Info(title,date,tel,sourceURL,priceURL,pageURL,city)

    def analyze_House_Price_Info(self):
        allProperties = data_manager.datamanager.find_Housedata_not_Analyzed()
        if allProperties is None:
            return
        for item in allProperties:
            url = item.get('sourceRegulation')
            titleName = item.get('title')
            rarFileDirectoryContent =  '/Users/kanglin/Python/house/%s' % (titleName)
            rarFile_Directory = os.path.dirname(rarFileDirectoryContent)
            file_name = '%s.rar' % (titleName)
            #下载房源价格rar包
            self.downloader.download_file(url,rarFile_Directory,file_name)
            #解压rar包
            rarPath = os.path.join(rarFile_Directory,file_name)
            unrarSavePath = self.localDataManager.un_rar(rarPath)
            print('rar路径')
            print(rarPath)
            #获取房源pdf的名字
            fileNames = self.localDataManager.getFileItemsFromFile(unrarSavePath)
            pdfFileName = None
            for name in fileNames:
                if "规则".decode('utf-8') not in name and "pdf" in name:
                    pdfFileName = name;
                    break;                
            #ocr识别pdf生成excel
            if (pdfFileName is None) == False:
                pafFilePath = os.path.join(unrarSavePath,pdfFileName)
                print('pdf路径')
                print(pafFilePath)
                self.pdfDealer.dealPDFHouseData(pafFilePath)



#可以新增一个检查重复的方法，有则只update下载地址,
#由于再进行检查会多一次网络请求，所以暂时不检查了，重复就取第一条

if __name__ == "__main__":
    
    #爬取成都公证处
    print('爬取成都公证处')
    rootURL = "http://www.cdgzc.com/gongshigonggao"
    spiderman = SpiderMain()
    # #爬取云盘地址
    spiderman.crow_page(rootURL,"成都")
    #2018-09-26 11:18:03
    #重置下载，百度云盘下载时间有8小时失效限制
    # spiderman.reset_data_notAnalyzed_to_notDownload()
    #获取Excel下载地址
    # spiderman.crow_download_excel_url()
    #分析Excel排名数据
    # spiderman.analyze_excel_ranking_data()

    #---------------------------
    #房协网
    print('爬取房协网')
    HosuseRootURL = "https://www.cdfangxie.com/Infor/type/typeid/36.html?&p=1"
    #爬取第一页的信息
    spiderman.crow_House_New_Info(HosuseRootURL,"成都")
    #解析房源价格信息
    spiderman.analyze_House_Price_Info()


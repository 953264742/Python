# encoding: utf-8
import leancloud
# 写在启动脚本的头部
# 如果是在 LeanEngine 环境，启动脚本是 wsgi.py
import logging
import xlrd
# import xlwt
import os
import constant
class DataManager(object):
    """docstring for DataManager"""
    def __init__(self):
        super(DataManager, self).__init__()
        #初始化leanCloud
        leancloud.init("kToaxnXoX3KCkdnNg6aYyyBi-gzGzoHsz", "4LgjRqFNEKYg7jaktALhoEjt")
        logging.basicConfig(level=logging.DEBUG)
        leancloud.use_region('CN') # 默认启用中国节点
        self.dataNotDonwLoad = []
        self.dataNotAnalyzed = []

    #找到最新的那一条数据
    def find_data_link_lastnew(self):
        YaoHaoRankingDataAddress = leancloud.Object.extend('YaoHaoRankingDataAddress')
        if YaoHaoRankingDataAddress:
            try:
                query = leancloud.Query(YaoHaoRankingDataAddress)
                query.add_descending("publishDate")
                find_property = query.first()
                if find_property:
                    return find_property
            except Exception as e:
                return None
            
        return None

    #根据链接找到数据
    def find_data_object_with_LinkURL(self,link_URL):
        YaoHaoRankingDataAddress = leancloud.Object.extend('YaoHaoRankingDataAddress')
        if YaoHaoRankingDataAddress:
            try:
                query = leancloud.Query(YaoHaoRankingDataAddress)
                query.equal_to("dataURL",link_URL)
                find_property = query.first()
                if find_property:
                    return find_property
            except Exception as e:
                return None
            
        
        return None

    #获取所有没有获取下载地址的excel的数据
    def find_all_data_not_download(self):
        if len(self.dataNotDonwLoad) > 0:
            return self.dataNotDonwLoad
        YaoHaoRankingDataAddress = leancloud.Object.extend('YaoHaoRankingDataAddress')
        if YaoHaoRankingDataAddress:
            try:
                query = leancloud.Query(YaoHaoRankingDataAddress)
                query.equal_to("isDownload",False)
                query.add_ascending("publishDate")
                find_property = query.find()
                if find_property:
                    self.dataNotDonwLoad = find_property
                    return self.dataNotDonwLoad
            except Exception as e:
                return None
        
        return None


    #获取没有解析Excel的数据,
    def find_data_not_analyzied(self):
        #查询过数据库后，直接返回数组中的数据
        if len(self.dataNotAnalyzed) > 0:
            find_property = self.dataNotAnalyzed.pop()
            return find_property

        #先查找数据库
        YaoHaoRankingDataAddress = leancloud.Object.extend('YaoHaoRankingDataAddress')
        if YaoHaoRankingDataAddress:
            try:
                query = leancloud.Query(YaoHaoRankingDataAddress)
                query.equal_to(constant.KISAnalyzed_Excel,False)
                query.add_ascending("publishDate")
                self.dataNotAnalyzed = query.find()
                if len(self.dataNotAnalyzed) == 0:
                    return None;
                find_property = self.dataNotAnalyzed.pop()
                return find_property

            except Exception as e:
                print(e)
                return None
            
        return None

 
    #获取没有解析Excel的数据,
    def find_all_data_not_analyzied(self):
        #先查找数据库
        YaoHaoRankingDataAddress = leancloud.Object.extend('YaoHaoRankingDataAddress')
        if YaoHaoRankingDataAddress:
            try:
                query = leancloud.Query(YaoHaoRankingDataAddress)
                query.equal_to(constant.KISAnalyzed_Excel,False)
                query.add_ascending("publishDate")
                find_properties = query.find()
                return find_properties

            except Exception as e:
                print(e)
                return None
            
        return None

    #解析Excel选房排名数据
    def analysis_excel_choseHouseOrder_data(self,name,callBack,title = "",date = ""):
        file_path = os.path.dirname("/Users/kanglin/Python/data/")
        local = os.path.join(file_path,name)
        # unicode_path = unicode(local,'utf-8')
        excel_file = xlrd.open_workbook(local)
        sheet = excel_file.sheet_by_index(0)
        rowCount = sheet.nrows

        data_array = []
        for i in range(1,rowCount):
            rowDataArray = sheet.row_values(i)
            order = rowDataArray[1]
            serial = rowDataArray[2]
            dic_item = {}
            dic_item[constant.KRank_Key] = order
            dic_item[constant.KSerial_Key] = serial
            dic_item[constant.KTitle_Key] = title
            dic_item[constant.KDate_Key] = date
            data_array.append(dic_item)

        callBack(data_array)


    """成都房协"""
    #找到最新的那一条数据
    def find_Housedata_lastnew(self):
        ChengduAssociationHouseData = leancloud.Object.extend('ChengduAssociationHouseData')
        if ChengduAssociationHouseData:
            try:
                query = leancloud.Query(ChengduAssociationHouseData)
                query.add_descending(constant.KDate_Key)
                find_property = query.first()
                if find_property:
                    return find_property
            except Exception as e:
                return None
            
        return None

    #找到所有没有分析的数据
    def find_Housedata_not_Analyzed(self):
        ChengduAssociationHouseData = leancloud.Object.extend('ChengduAssociationHouseData')
        if ChengduAssociationHouseData:
            try:
                query = leancloud.Query(ChengduAssociationHouseData)
                query.add_descending(constant.KDate_Key)
                query.equal_to(constant.KPropject_isAnalyzed,False)
                find_property = query.find()
                if find_property:
                    return find_property
            except Exception as e:
                print e
                return None
            
        return None

datamanager = DataManager()

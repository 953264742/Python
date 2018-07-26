# encoding: utf-8
import leancloud
# 写在启动脚本的头部
# 如果是在 LeanEngine 环境，启动脚本是 wsgi.py
import logging

class DataManager(object):
    """docstring for DataManager"""
    def __init__(self):
        super(DataManager, self).__init__()
        #初始化leanCloud
        leancloud.init("kToaxnXoX3KCkdnNg6aYyyBi-gzGzoHsz", "4LgjRqFNEKYg7jaktALhoEjt")
        logging.basicConfig(level=logging.DEBUG)
        leancloud.use_region('CN') # 默认启用中国节点
        self.data_need_download = self.find_all_data_not_download()

    #找到最新的那一条数据
    def find_data_link_lastnew(self):
        YaoHaoRankingDataAddress = leancloud.Object.extend('YaoHaoRankingDataAddress')
        if YaoHaoRankingDataAddress:
            query = leancloud.Query(YaoHaoRankingDataAddress)
            query.add_descending("publishDate")
            find_property = query.first()
            if find_property:
                return find_property
        
        return None

    #根据链接找到数据
    def find_data_object_with_LinkURL(self,link_URL):
        YaoHaoRankingDataAddress = leancloud.Object.extend('YaoHaoRankingDataAddress')
        if YaoHaoRankingDataAddress:
            query = leancloud.Query(YaoHaoRankingDataAddress)
            query.equal_to("dataURL",link_URL)
            find_property = query.first()
            if find_property:
                return find_property
        
        return None

    #获取所有没有下载excel的数据
    def find_all_data_not_download(self):
        YaoHaoRankingDataAddress = leancloud.Object.extend('YaoHaoRankingDataAddress')
        if YaoHaoRankingDataAddress:
            query = leancloud.Query(YaoHaoRankingDataAddress)
            query.equal_to("isDownload",False)
            find_property = query.find()
            if find_property:
                return find_property
        
        return None

datamanager = DataManager()

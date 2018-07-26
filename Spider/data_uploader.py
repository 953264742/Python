# encoding: utf-8
#appid:kToaxnXoX3KCkdnNg6aYyyBi-gzGzoHsz
#appkey:4LgjRqFNEKYg7jaktALhoEjt
#masterKey:3U3JwwUaCGIUnxACJjvyCfrj

import leancloud
# 写在启动脚本的头部
# 如果是在 LeanEngine 环境，启动脚本是 wsgi.py
import logging
import data_manager
import constant


class DataUploader(object):
    """docstring for ClassName"""
    def __init__(self):
        super(DataUploader, self).__init__()
        #初始化leanCloud
        # leancloud.init("kToaxnXoX3KCkdnNg6aYyyBi-gzGzoHsz", "4LgjRqFNEKYg7jaktALhoEjt")
        # logging.basicConfig(level=logging.DEBUG)
        # leancloud.use_region('CN') # 默认启用中国节点

    def upload_data_save_url(self,dataURL,city,publishDate,isDownload,rootURL,excelYunPanURL):
        TodoFolder = leancloud.Object.extend('YaoHaoRankingDataAddress')
        todo_folder = TodoFolder()
        todo_folder.set(constant.KLink_URL_Key, dataURL)
        todo_folder.set(constant.KLink_URL_Key, city)
        todo_folder.set(constant.KPublish_Key, publishDate)
        todo_folder.set(constant.KIsDownload_Key, isDownload)
        todo_folder.set(constant.KRootURL,rootURL)
        todo_folder.set(constant.KExcel_Yun_URL,excelYunPanURL)
        todo_folder.set(constant.KExcel_download_URL, [])

        todo_folder.save()
    def update_data_withExcelDownloadURL(self,yun_object,excelDownLoadURL,title):
        if yun_object is None:
            print('云对象为空')
            return;
        if excelDownLoadURL is None:
            print('下载的url地址为空')
            return;
        link_Url = yun_object.get(constant.KLink_URL_Key)
        current_yun_object = data_manager.datamanager.find_data_object_with_LinkURL(link_Url)
        before_DownLoad_URL = current_yun_object.get(constant.KExcel_download_URL)
        print('before_DownLoad_URL',before_DownLoad_URL)
        if before_DownLoad_URL:
            before_DownLoad_URL.append({constant.KBuilding_Yun_URL:excelDownLoadURL,constant.KBuilding_title:title})
            yun_object.set(constant.KExcel_download_URL, before_DownLoad_URL)
        else:
            yun_object.set(constant.KExcel_download_URL, [{constant.KBuilding_Yun_URL:excelDownLoadURL,constant.KBuilding_title:title}])
        yun_object.set(constant.KIsDownload_Key, True)
        yun_object.save()



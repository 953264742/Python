# encoding: utf-8

#!/usr/bin/env python

import rarfile
import os

class LocalDataManager(object):
    """docstring for LocalDataManager"""
    def __init__(self):
        super(LocalDataManager, self).__init__()


    def un_rar(self,filePath):
        """unrar zip file"""
        print('开始解压rar文件')
        print(filePath)
        rar = rarfile.RarFile(filePath)
        head,fileName = os.path.split(filePath)
        saveDirectory = filePath.replace(".rar","")
        print(saveDirectory)
        list = rar.namelist()
        print(list)

        rar.extractall(saveDirectory)
        rar.close()
        return saveDirectory


    """返回文件路径中所有文件"""
    def getFileItemsFromFile(self,filePath):
        return os.listdir(filePath)


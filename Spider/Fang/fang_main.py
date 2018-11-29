
# encoding: utf-8

#!/usr/bin/env python
# import tabula
import os
import pdfplumber
import pandas as pd
import cv2
from aip import AipOcr
import base64
import json
import xlwt
import os
import ntpath
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def print_j(str):
    print json.dumps(str, ensure_ascii=False, indent=2)

""" 你的 APPID AK SK """
APP_ID = '14298766'
API_KEY = 'cepdRc9BaqbNpP5BP0YCYfpG'
SECRET_KEY = 'OqZQGXusGmRjLb7N1TYszcpFQD43p26l'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

class PDF_Data_Dealer(object):
    """docstring for PDF_Data_Dealer"""
    def __init__(self,localDataManager):
        super(PDF_Data_Dealer, self).__init__()
        self.localDataManager = localDataManager

    #将pdf转为图片，
    def savePdfToImages(self,fromPath,saveDirectory):
        print('读取pdf文件路径')
        print(fromPath)
        print('图片存储路径')
        print(saveDirectory)
        head,fileName = os.path.split(fromPath)
        fileName = fileName.replace('.pdf',"").encode('utf-8')

        pdf = pdfplumber.open(fromPath)
        if os.path.exists(saveDirectory) == False:
            os.makedirs(saveDirectory)

        i = 0
        for page in pdf.pages:
            imageName = '%s_%s.jpg' % (fileName,i)
            imageSavePath =  os.path.join(saveDirectory,imageName)
              #文件已存在不再转为图片
            if os.path.isfile(imageSavePath):
                break;
            im = page.to_image(resolution=130)
            im.save(imageSavePath,format='jpeg')
            i += 1
        
        

    """ 读取图片 """
    def scanPdfToJson(self,filePath,jsonSaveDirectory):

        # for i in range(0,numberOfPages):
        imagePath = filePath
        print("图片路径")
        print(imagePath)
        #获取json文件名称
        head,fileName = ntpath.split(filePath)
        fileNameWithoutExtention = fileName.replace(".jpg","")
        jsonName = '%s.json' % (fileNameWithoutExtention)
        if not os.path.exists(jsonSaveDirectory):
            os.makedirs(jsonSaveDirectory)

        savePath = os.path.join(jsonSaveDirectory,jsonName)

        #json文件已存在，不再识别
        if os.path.isfile(savePath):
            print('json文件已存在，不再识别')
            print(savePath)
            return

        with open(imagePath,"rb") as f:
            # image = base64.b64encode(f.read()) 
            image = f.read()
            print('开始识别...')
            result = client.form(image);
            print('识别结果')
            print_j(result)
            try:
                body = result['forms_result']

                if len(body) > 0:
                    self.saveJsonToPath(body,savePath)
            except Exception as e:
                # errorcode = result['error_code']
                # print('errorcode',errorcode)
                # print("重新识别")
                # #error_msg": "Service temporarily unavailable",
                # #没有识别到、继续重新识别
                # if errorcode == 2:
                #     self.scanPdfToJson(filePath,jsonSaveDirectory)
                # print(e)
                pass
            else:
                pass
            finally:
                pass
            
    """ json写入文件 """
    def saveJsonToPath(self,jsonContent,filePath):
        with open(filePath,"w") as f:
            json.dump(jsonContent,f)
            print('json写入成功')

    """ 读取json从文件 """
    def redJson(self,filePath):
        if os.path.isfile(filePath) == False:
            return None;
        with open(filePath,'r') as f:
            jsonData = json.load(f)
            print('加载的json')
            print_j(jsonData)
            return jsonData

    """ 把json转为excel表格 """
    def createJsonToExcel(self,filePath,excelSaveDirectory):
        datas = self.redJson(filePath)
        if datas is None:
            print('readJsonEmpty:',filePath)
            return

        head,jsonName = ntpath.split(filePath)
        excelName = jsonName.replace('json','xls')
        savePath = os.path.join(excelSaveDirectory,excelName)
        if not os.path.exists(excelSaveDirectory):
            os.makedirs(excelSaveDirectory)

        book = xlwt.Workbook() #创建excel对象
        sheet = book.add_sheet('Sheet1',cell_overwrite_ok=True)
        print("开始创建EXCEL")
        body = datas[0]['body']
        for item in body:
            try:
                column = item['column']
                row = item['row']
                content = item['words']
                print('EXCEL_content',content)
                sheet.write(row,column,content)
            except Exception as e:
                print(e)
            else:
                pass
            
        book.save(savePath)
        print(savePath)
        print("Excel创建成功")

    def dealPDFHouseData(self,pdfPath):

        image_save_directory = pdfPath
        head,fileName = os.path.split(image_save_directory)
        #图片存储存根目录
        image_save_directory = image_save_directory.replace(fileName,"")
        #图片存储的文件夹路径
        imageSaveDirectory = '%simages/' % (image_save_directory)
        #json存储的文件夹路径
        jsonSaveDirectory = '%sjsons/' % (imageSaveDirectory)
        #excel存储的文件夹路径
        excelSaveDirectory = '%sexcels/' % (imageSaveDirectory)

        self.savePdfToImages(pdfPath,imageSaveDirectory)
        allFiles = self.localDataManager.getFileItemsFromFile(imageSaveDirectory)
        for fileName in allFiles:
            if "jpg" not in fileName :
                continue;
            imageFilePath = os.path.join(imageSaveDirectory,fileName)
            fileBeforeName = fileName.replace(".jpg","")
            jsonName = '%s.json' % (fileBeforeName)
            json_savePath = os.path.join(jsonSaveDirectory,jsonName)
            
            #把pdf读取为json并存储在本地
            self.scanPdfToJson(imageFilePath,jsonSaveDirectory)
            excelName =  '%s.xls' % (fileBeforeName)
            excel_savePath = os.path.join(excelSaveDirectory,excelName)

            #如果已经生成了excel则跳过
            if os.path.isfile(excel_savePath):
                continue;
            #生成excel文件
            self.createJsonToExcel(json_savePath,excelSaveDirectory)

# if __name__ == "__main__":
    # pdfDealer = PDF_Data_Dealer()
    # #打开路径
    # file_path = os.path.dirname("/Users/kanglin/Python/data/")
    # local = os.path.join(file_path,"金科博翠粼湖楼盘表.pdf")
    # #图片存储存储路径
    # save_root_path = os.path.dirname("/Users/kanglin/Python/images/")
    # savePath = os.path.join(save_root_path,"form0.jpg")
    # #json存储路径
    # json_root_path = os.path.dirname("/Users/kanglin/Python/jsons/")
    # json_savePath = os.path.join(save_root_path,"form0.json")

    # pdfDealer.savePdfToImages(local,save_root_path)
    # pdfDealer.get_file_content(savePath)
    # pdfDealer.createJsonToExcel(json_savePath)

  
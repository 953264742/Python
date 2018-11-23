#encoding:utf-8
import urllib
import urllib2
import os
import ssl


class HtmlDownloader(object):
    """docstring for HtmlDownloader"""
    def __init__(self):
        super(HtmlDownloader, self).__init__()

    def download(self,url):
        if url is None:
            return None

        context = None
        if url.startswith('https'):
            context = ssl._create_unverified_context()
        response = urllib2.urlopen(url,context=context)

        if response.getcode() != 200:
            return None
        return response.read()

    def progress(self,a,b,c):
        per = 100.0 * a * b / c
        if per > 100 :
             per = 100
        print ('%.2f%%' % per)

    def download_file(self,url,saveDirectory,name):
        local = os.path.join(saveDirectory,name)
        print('loalExcel',local)
        if os.path.isfile(local):
            print('想要下载的文件文件已存在')
            return;
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib.urlretrieve(url,local,self.progress)



#encoding:utf-8
import urllib
import urllib2
import os



class HtmlDownloader(object):
    """docstring for HtmlDownloader"""
    def __init__(self):
        super(HtmlDownloader, self).__init__()

    def download(self,url):
        if url is None:
            return None

        response = urllib2.urlopen(url)

        if response.getcode() != 200:
            return None
        return response.read()

    def progress(self,a,b,c):
        per = 100.0 * a * b / c
        if per > 100 :
             per = 100
        print '%.2f%%' % per

    def download_excel(self,url,name):
        file_path = os.path.dirname("/Users/kanglin/Python/data/")
        local = os.path.join(file_path,name)
        urllib.urlretrieve(url,local,self.progress)



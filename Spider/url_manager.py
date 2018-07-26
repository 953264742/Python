
# encoding: utf-8

class UrlManager(object):
    """docstring for UrlManager"""
    def __init__(self):
        super(UrlManager, self).__init__()
        #新爬取的url
        self.new_urls = []
        #网站数据点击的地址
        self.detail_urls = []
        #爬取过的url
        self.old_urls = []

    #每一个page的url存储
    def append_url(self,url):
        if url is None:
            return
        if url  in self.new_urls or url  in self.old_urls:
            return
        self.new_urls.append(url)

    def append_urls(self,urls):
        if urls is None:
            return 
        if len(urls) == 0:
            return
        for url in urls:
            self.append_url(url)

    def has_url(self):
        if len(self.new_urls) == 0:
            return False
        return True

    def get_url(self):
        url  = self.new_urls.pop()
        self.old_urls.append(url)
        return url

    #详情数据的url存储
    def append_detail_url(self,url):
        if url is None:
            return
        if url  in self.detail_urls or url  in self.old_urls:
            return
        self.detail_urls.append(url)

    def append_detail_urls(self,urls):
        if urls is None:
            return 
        if len(urls) == 0:
            return
        for url in urls:
            self.append_detail_url(url)

    def has_detail_url(self):
        if len(self.detail_urls) == 0:
            return False
        return True

    def get_detail_url(self):
        url  = self.detail_urls.pop()
        self.old_urls.append(url)
        return url

    def clear_urls(self):
        self.new_urls.clear()
        self.old_urls.clear()
        self.detail_urls.clear()


# encoding: utf-8


class HtmlOutputer(object):
    """docstring for HtmlOutputer"""
    def __init__(self):
        super(HtmlOutputer, self).__init__()
        self.baidu_pan_excel_urls = []
        self.download_urls = []
    def collect(self,urls):
        if urls is None or len(urls) == 0:
            return

        for url in urls:
            self.baidu_pan_excel_urls.append(url)

    def collect_download_url(self,url):
            self.download_urls.append(url)

    def output(self):
        for url in self.baidu_pan_excel_urls:
            print(unicode("我收集到的所有EXcel地址", encoding="utf-8"))
            print(url)

    def output_download_url(self):
        for url in self.download_urls:
            print(unicode("所有EXcel下载地址", encoding="utf-8"))
            print(url)
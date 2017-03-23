#coding:utf-8
import url_manager, html_downLoader, html_parser, html_outputer
import robotparser
import disk_cache
import logging
import mongo_cache
import sys
if sys.getdefaultencoding()!="utf-8":
    reload(sys)
    sys.setdefaultencoding("utf-8")

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.Url_Manager()
        self.downloader = html_downLoader.HtmlDownLoader()
        self.parser = html_parser.HtmlParser()
        self.outper = html_outputer.OutPuter()
        #self.cache=disk_cache.DiskCache()
        self.cache=mongo_cache.MongoCache()

    def craw_isrunning(self,new_url):
        if self.cache[new_url] is not None:
            #print self.cache[new_url]
            html_cont=self.cache[new_url]
        else:
             #以上代码正常
            html_cont = self.downloader.downLoad(new_url)
            html_cont=html_cont.decode("unicode_escape")
            #print html_cont
            self.cache[new_url]=html_cont
        new_urls, new_data = self.parser.parse(new_url,html_cont)
         # for seturl in new_urls:
         # print 'seturl:%s'%(seturl)
        # print new_urls
        # print new_data
        self.urls.add_new_urls(new_urls)
        self.outper.collect_data(new_data)

    def craw(self, rool_url):
        count = 1
        self.urls.add_new_url(rool_url)
        throttle=self.downloader.Throttle(0)
        rp=robotparser.RobotFileParser()
        rp.set_url('https://baike.baidu.com/robots.txt')
        rp.read()
        user_agent='wswp'
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print u'第%d个页面%s'%(count,new_url)
                if True:#rp.can_fetch(user_agent,new_url):
                    #print "if is running"
                    throttle.wait(new_url)
                    self.craw_isrunning(new_url)
                    if count == 20:
                        break
                    count = count + 1
                else:
                     print 'Blocked by robots.txt',new_url
            except Exception, e:
                print 'craw failed'
                print e.message
        self.outper.output_html()
        # for oldurl in self.urls.old_urls:
        #     print 'oldurl%s:' % (oldurl)
        # for newurl in self.urls.new_urls:
        #     print 'newurl%s:' % (newurl)

if __name__ == '__main__':
    rool_url = "http://example.webscraping.com"
    obj_spider = SpiderMain()
    obj_spider.craw(rool_url)

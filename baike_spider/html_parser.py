#coding:utf-8
import urlparse
from bs4 import BeautifulSoup
import re

class HtmlParser(object):
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup=BeautifulSoup(html_cont,"html.parser")
        new_urls=self.get_new_urls(page_url,soup)
        new_data=self.get_new_data(page_url,html_cont)
        return new_urls,new_data

    def get_new_urls(self,page_url, soup):
        #print 'page_url:%s' %(page_url)
        new_urls=set()
        links=soup.find_all('a',href=re.compile(r'/(index|view)'))
        for link in links:
            new_url=link['href']
            #print 'new_url:%s' %(new_url)
            new_full_url=urlparse.urljoin(page_url,new_url)
            #print 'new_full_url:%s' %(new_full_url)
            new_urls.add(new_full_url)
        return new_urls

    def get_new_data(self, page_url, html_cont):
        res_data={}
        #url
        res_data['url']=page_url
        # #<dd class="lemmaWgt-lemmaTitle-title"><h1>Python</h1>
        # tite_node=soup.find('dd',class_="lemmaWgt-lemmaTitle-title").find('h1')
        # res_data['title']=tite_node.get_text()
        # #<div class="lemma-summary" label-module="lemmaSummary">
        # summary_node=soup.find('div',class_="lemma-summary")
        # res_data['summary']=summary_node.get_text()
        res_data["html"]=html_cont
        return res_data
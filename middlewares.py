# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from dataclasses import field
from subprocess import CREATE_NEW_CONSOLE
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from scrapy.http.response.html import HtmlResponse
import json
from selenium.webdriver.common.by import By

class LuckknightspiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    
    def process_request(self, request, spider):
        if request.url.__contains__('www.belk.com/search/?prefn1=groupedEventCodeID&prefv1=22BFSDB'):
            try:
                spider.driver.get(request.url)
                time.sleep(10)
                pageData = spider.driver.execute_script('return window.pageData')
                nexturl=spider.driver.find_element(By.XPATH,'//*[@class="page-next"]').get_attribute("href")
                new_body={"page_data":json.dumps(pageData["products"]),"next_url":nexturl}
                response = HtmlResponse(
                    url=spider.driver.current_url,
                    body=json.dumps(new_body).encode(),
                    request=request,
                    encoding="utf-8"
                )
                return response
            except Exception as e:
                print(e)
                return None
        return None
        
    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass
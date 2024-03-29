# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
from selenium import webdriver

from scrapy import signals
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger
import requests


class PdsuSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self,timeout=None, service_args=[]):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        """
        self.browser = webdriver.PhantomJS(service_args=service_args)
        self.browser.set_window_size(1400, 700)
        self.browser.set_page_load_timeout(self.timeout)
        """
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        self.logger.debug('browser is starting')
        try:
            #chrome_options = webdriver.ChromeOptions()
            #chrome_options.add_argument('--proxy-server=' + request.meta['proxy'])
            #self.browser = self.browser(chrome_options=chrome_options)
            #self.logger.debug("proxy,cookies", request.cookies, request.meta['proxy'])
            self.browser.get(request.url)
            self.browser.add_cookie(request.cookies)
            self.browser.get(request.url)
            self.browser.switch_to.frame('frmbody')
            select = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#memuBarText1 > b')))
            select.click()
            select = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#memuLinkDiv1 > table > tbody > tr:nth-child(2) > td:nth-child(2)')))
            select.click()
            select = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#divGrpD0102 > td > table > tbody > tr:nth-child(1) > td:nth-child(2)')))
            select.click()
            self.browser.switch_to.frame('frmMain')
            self.browser.switch_to.frame('main')
            user = self.browser.page_source
            self.browser.switch_to.parent_frame()
            self.browser.switch_to.parent_frame()
            select = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#memuBarText4 > b')))
            select.click()
            select = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#memuLinkDiv4 > table > tbody > tr:nth-child(1) > td:nth-child(2) > span')))
            select.click()
            self.browser.switch_to.frame('frmMain')
            select = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#rad_gs1')))
            select.click()
            select = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'body > form > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > input:nth-child(1)')))
            select.click()
            self.browser.switch_to.frame('frmRpt')
            usertimetable = self.browser.page_source
            self.browser.switch_to.parent_frame()
            self.browser.switch_to.parent_frame()
            select = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#memuBarText6 > b')))
            select.click()
            select = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#memuLinkDiv6 > table > tbody > tr:nth-child(6) > td:nth-child(2) > span')))
            select.click()
            self.browser.switch_to.frame('frmMain')
            select = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'body > form > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td:nth-child(3) > input.button')))
            select.click()
            self.browser.switch_to.frame('main')
            userscore = self.browser.page_source
            page_source = user+usertimetable+userscore
            return HtmlResponse(url=request.url, body=page_source, request=request, encoding='utf-8',status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class PdsuDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
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

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CookiesMiddleware():
    def __init__(self, cookies_url):
        self.logger = getLogger(__name__)
        self.cookies_url = cookies_url

    def get_random_cookies(self):
        try:
            response = requests.get(self.cookies_url)
            if response.status_code == 200:
                cookies = json.loads(response.text)
                for key, value in cookies.items():
                    cookies = {'name': key, 'value': value}
                return cookies
        except requests.ConnectionError:
            return False

    def process_request(self,request,spider):
        self.logger.debug('正在获取cookies')
        cookies = self.get_random_cookies()
        if cookies:
            request.cookies = cookies
            self.logger.debug('使用cookies'+json.dumps(cookies))

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        settings = crawler.settings
        return cls(
            cookies_url=settings.get('COOKIES_URL')
        )


class ProxyMiddleware():
    def __init__(self, proxy_url):
        self.logger = getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        proxy = self.get_random_proxy()
        if proxy:
            uri = 'https://{proxy}'.format(proxy=proxy)
            self.logger.debug('使用代理'+proxy)
            request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )

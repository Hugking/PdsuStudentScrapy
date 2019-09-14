# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from pdsu.items import UserItem,UsertimetableItem,UserscoreItem
import logging

class PdsuSpider(CrawlSpider):
    name = 'pdsu'
    allowed_domains = ['jiaowu.pdsu.edu.cn']
    start_urls = ['http://jiaowu.pdsu.edu.cn/MAINFRM.aspx']

    def parse(self, response):
        """
        解析用户信息
        :param response: Response对象
        """
        useritem = UserItem()
        useritem['stunum'] = ''.join(response.xpath('/html/body/center[1]/table/tbody/tr[2]/td[2]//text()').extract()).strip()
        useritem['name'] = ''.join(response.xpath('/html/body/center[1]/table/tbody/tr[2]/td[4]//text()').extract()).strip()
        useritem['department'] = ''.join(response.xpath('/html/body/center[1]/table/tbody/tr[24]/td[2]//text()').extract()).strip()
        useritem['major'] = ''.join(response.xpath('/html/body/center[1]/table/tbody/tr[24]/td[4]//text()').extract()).strip()
        useritem['classes'] = ''.join(response.xpath('/html/body/center[1]/table/tbody/tr[24]/td[6]//text()').extract()).strip()
        usertimeitem = UsertimetableItem()
        usertimeitem['timetable'] = ''.join(response.xpath('//*[@id="pageRpt"]/div/div/img/@src').extract()).strip()
        usertimeitem['remark'] = ''.join(response.xpath('//*[@id="pageRpt"]/table/tbody/tr/td[2]//text()').extract()).strip().replace('\u2002', '')
        usertimeitem['time'] = ''.join(response.xpath('//*[@id="tn2"]//text()').extract()).strip()
        userscoreitem = UserscoreItem()
        userscoreitem['department'] = ''.join(response.xpath('//center/table[2]/tbody/tr[1]/td[1]//text()').extract()).strip().replace('院(系)/部：', '')
        userscoreitem['classes'] = ''.join(response.xpath('//center/table[2]/tbody/tr[1]/td[2]//text()').extract()).strip().replace('行政班级：', '')
        userscoreitem['average'] = ''.join(response.xpath('//center/table[2]/tbody/tr[1]/td[3]//text()').extract()).strip().replace('平均学分绩点：', '')
        userscoreitem['stunum'] = ''.join(response.xpath('//center/table[2]/tbody/tr[2]/td[1]//text()').extract()).strip().replace('\u2002', '').replace('学号：', '')
        userscoreitem['name'] = ''.join(response.xpath('//center//table[2]/tbody/tr[2]/td[2]//text()').extract()).strip().replace('\u2002', '').replace('姓名：', '')
        userscoreitem['looktime'] = ''.join(response.xpath('//center/table[2]/tbody/tr[2]/td[3]//text()').extract()).strip().replace('打印时间：', '')
        userscoreitem['time'] = ''.join(response.xpath('//center/table[3]/tbody/tr/td//text()').extract()).strip().replace('学年学期：', '')
        userscoreitem['score'] = ''.join(response.xpath('//center/div/div/img/@src').extract()).strip()
        yield useritem
        yield usertimeitem
        yield userscoreitem

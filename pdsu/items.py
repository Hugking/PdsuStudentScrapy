# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class UserItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'user'
    stunum = Field()
    name = Field()
    department = Field()
    major = Field()
    classes = Field()

class UsertimetableItem(Item):
    collection = 'usertimetable'
    timetable = Field()
    remark = Field()
    time = Field()

class UserscoreItem(Item):
    collection = 'userscore'
    department = Field()
    classes = Field()
    average = Field()
    stunum = Field()
    name = Field()
    looktime = Field()
    time = Field()
    score = Field()


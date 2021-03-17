# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class RealestateScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type = scrapy.Field()
    typeOfOffer = scrapy.Field()
    city = scrapy.Field(default='NULL')
    municipality = scrapy.Field(default='NULL')
    squareFootage = scrapy.Field(default=0)
    constructionYear = scrapy.Field(default=0)
    landArea = scrapy.Field(default='NULL')
    floorInfo = scrapy.Field(default='NULL')
    registration = scrapy.Field(default='NULL')
    heatingType = scrapy.Field(default='NULL')
    roomNo = scrapy.Field(default=0)
    bathroomNo = scrapy.Field(default='NULL')
    price = scrapy.Field(default=0)
    country = scrapy.Field(default='NULL')
    con = scrapy.Field(default='NULL')
    pl = scrapy.Field(default='NULL')
    pumpaIliKalorimetri = scrapy.Field(default='NULL')
    #pass

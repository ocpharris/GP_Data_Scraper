# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass



class GpItem(scrapy.Item):
    name = scrapy.Field()
    accepting_patients = scrapy.Field()
    phone_number = scrapy.Field()
    miles_away = scrapy.Field()
    gp_website = scrapy.Field()
    in_catchment = scrapy.Field()
    gp_address = scrapy.Field()
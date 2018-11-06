# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


from scrapy.item import Item, Field

class CarItem(Item):
    make = Field()
    model = Field()
    year = Field()
    transmission = Field()
    mileage = Field()
    price = Field()
    location = Field()
    full_name = Field()
    description = Field()
    date_posted = Field()
    link = Field()

    def __str__(self):
        return self['full_name']
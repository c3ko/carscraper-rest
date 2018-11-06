# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from car_scraper.items import CarItem




class KijijiSpider(CrawlSpider):
    name = 'KijijiCar'

    def __init__(self, make='', model='', **kwargs):
        self.make = make
        self.model = model
        self.allowed_domains = ['kijiji.ca']
        self.start_urls = [f"""https://www.kijiji.ca/b-cars-trucks/gta-greater-toronto-area/{make}-{model}
                      /k0c174l1700272"""]
        super().__init__(**kwargs)

    def parse(self, response):

        for car_page_url in response.xpath('//a[@class="title enable-search-navigation-flag "]/@href').extract():
            print(car_page_url)
            yield scrapy.Request(url=response.urljoin(car_page_url), callback=self.parse_car)

        next_page_url = response.css('div.bottom-bar > div.pagination > a:nth-last-child(2)::attr(href)').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_car(self, page_response):
        item = CarItem()
        item['year'] = page_response.xpath('//dd[@itemprop="vehicleModelDate"]/text()').extract_first()
        item['make'] = page_response.xpath('//dd[@itemprop="brand"]/text()').extract_first()
        item['model'] = page_response.xpath('//dd[@itemprop="model"]/text()').extract_first()
        mileage = page_response.xpath('//dd[@itemprop="mileageFromOdometer"]/text()').extract_first()
        item['mileage'] = str(mileage).replace(',', '')
        item['transmission'] = page_response.xpath('//dd[@itemprop="vehicleTransmission"]/text()').extract_first()
        item['location'] = page_response.xpath('//span[@itemprop="address"]/text()').extract_first()
        price = page_response.xpath('//span[@itemprop="price"]/text()').extract_first()
        item['price'] = str(price).replace('$', '').replace(',', '')
        #remove last 5 characters i.e timezone '.000Z' from datetime
        item['date_posted'] = page_response.xpath('//time/@datetime').extract_first()[:-5]
        item['full_name'] = page_response.xpath('//h1[@itemprop="name"]/text()').extract_first()
        item['description'] = page_response.xpath('//div[@itemprop="description"]/text()').extract_first()
        item['link'] = page_response.url
        yield item

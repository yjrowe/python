# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem
from scrapy.http import Request

class TencentpositionSpider(scrapy.Spider):
    name = 'tencentPosition'
    allowed_domains = ['tencent.com']
    baseUrl = 'http://hr.tencent.com/position.php?&start='
    offset = 0
    start_urls = ['http://hr.tencent.com/position.php?&start=0']

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

        for node in node_list:
            item = TencentItem()
            item['positionName'] = node.xpath("./td[1]/a/text()").extract()[0]
            item['positionLink'] = 'http://hr.tencent.com/' + node.xpath("./td[1]/a/@href").extract()[0]
            if len(node.xpath("./td[2]/text()")):
                item['positionType'] = node.xpath("./td[2]/text()").extract()[0]
            else:
                item['positionType'] = ''
            item['peopleNumber'] = node.xpath("./td[3]/text()").extract()[0]
            item['workLocation'] = node.xpath("./td[4]/text()").extract()[0]
            item['publishTime'] = node.xpath("./td[5]/text()").extract()[0]
            yield item

        total = int(response.xpath("//span[@class='lightblue total']/text()").extract()[0])

        if self.offset < total:
            self.offset += len(node_list)
            url = self.baseUrl + str(self.offset)
            yield Request(url = url, callback = self.parse)
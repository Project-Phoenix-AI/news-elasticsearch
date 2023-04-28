from pathlib import Path

import scrapy


class Spider(scrapy.Spider):
    name = "article"

    def start_requests(self, url, **kwargs):
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        allText = response.xpath('//article//p/text()|//article//p/b/text()')
        
        for txt in allText:
            print("txt:::: " + txt.get())
        
        for txt in allText:
            try:
                yield self.output_callback({
                    'name': txt.xpath('//h3/text()|./text()').get().strip(),
                    'link': txt.xpath('./@href').get().strip(),
                })
            except:
                print("Empty")

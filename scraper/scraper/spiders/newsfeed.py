from pathlib import Path

import scrapy


class Spider(scrapy.Spider):
    name = "newsfeed"

    def start_requests(self):
        urls = [
            'https://www.bbc.com/',
            'https://www.bbc.com/news',
            'https://www.bbc.com/sport'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        allNews = response.xpath('//div[contains(@class, "module__content")]//ul/li//a[contains(@class, "media__link")]|//div[contains(@id, "site-container")]//a[starts-with(@class, "gs-c-promo-heading")]')
        for news in allNews:
            print("news:::: " + news.get())
        
        for news in allNews:
            name = news.xpath('./text()').get().strip()
            

            try:
                yield {
                    'name': news.xpath('/h3/text()|./text()').get().strip(),
                    'link': news.xpath('./@href').get().strip(),
                }
            except:
                yield {
                    'name': "none",
                    'link': "none",
                }

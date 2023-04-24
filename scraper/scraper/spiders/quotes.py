from pathlib import Path

import scrapy


class Spider(scrapy.Spider):
    name = "newsfeed"

    def start_requests(self):
        urls = [
            'https://www.bbc.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        allNews = response.xpath('//section[contains(@class, "module module--promo")]/div/ul/li//a[contains(@class, "media__link")]|//section[contains(@class, "module module--content")]/div/ul/li//a[contains(@class, "media__link")]')
        print("allnews:::: " + allNews.get())
        
        for news in allNews:
            try:
                yield {
                    'name': news.xpath('text()').extract(),
                    #'link': news.css('a::href').get(),
                }
            except:
                yield {
                    'name': "none",
                    #'link': "none",
                }

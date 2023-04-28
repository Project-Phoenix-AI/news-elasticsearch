from pathlib import Path

import scrapy


class Spider(scrapy.Spider):
    name = "newsfeed"

    def start_requests(self, **kwargs):
        urls = [
            'https://www.bbc.com/',
            'https://www.bbc.com/news',
            'https://www.bbc.com/sport'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        allNews = response.xpath('//div[contains(@class, "module__content")]//ul/li//a[contains(@class, "media__link")]|//div[contains(@id, "site-container")]//a[starts-with(@class, "gs-c-promo-heading")]')
        #for news in allNews:
        #    print("news:::: " + news.get())
        
        for news in allNews:
            name = news.xpath('//h3/text()|./text()').get().strip()
            link = news.xpath('./@href').get().strip()

            if(link.split("/")[0] != "https:"):
                link = "https://www.bbc.com" + link

            txt = yield scrapy.Request(url=link, callback=self.parse_article)

            print("This is txt")
            print(txt)

            try:
                yield self.output_callback({
                    'name': news.xpath('//h3/text()|./text()').get().strip(),
                    'link': news.xpath('./@href').get().strip(),
                    'text': txt
                })
            except:
                print("Empty")

    def parse_article(self, response):

            article = response.xpath('//article//p/text()|//article//p/b/text()')

            text = ""

            for txt in article:
                text = text + txt.get()

            print(text)

            return text


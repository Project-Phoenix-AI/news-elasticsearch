from pathlib import Path

import scrapy


class Spider(scrapy.Spider):
    name = "newsfeed"

    def start_requests(self, **kwargs):
        urls = [
            'https://www.bbc.com/',
            'https://www.bbc.com/news',
            'https://www.bbc.com/sport',
            'https://www.bbc.com/news/world-60525350',
            'https://www.bbc.com/news/topics/c9wl4m5rqmlt',
            'https://www.bbc.com/news/av/10462520',
            'https://www.bbc.com/news/science-environment-56837908',
            'https://www.bbc.com/news/uk',
            'https://www.bbc.com/news/business',
            'https://www.bbc.com/news/technology',
            'https://www.bbc.com/news/science_and_environment',
            'https://www.bbc.com/news/stories'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        allNews = response.xpath('//div[contains(@class, "module__content")]//ul/li//a[contains(@class, "media__link")]|//div[contains(@id, "site-container")]//a[starts-with(@class, "gs-c-promo-heading")]')
        #for news in allNews:
        #    print("news:::: " + news.get())
        
        for news in allNews:
            link = news.xpath('./@href').get().strip()

            if(link.split("/")[0] != "https:"):
                link = "https://www.bbc.com" + link

            yield scrapy.Request(url=link, callback=self.parse_article)

    def parse_article(self, response):
            article = response.xpath('//article//p/text()|//article//p/b/text()|//article//p/span/text()')
            name = response.xpath('//article//h1/text()|//div//h1/text()').get()


            text = ""

            for txt in article:
                text = text + txt.get()

            try:
                yield self.output_callback({
                    'name': name,
                    'link': response.request.url,
                    'text': text
                })
            except:
                print("Empty")

            
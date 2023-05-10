from pathlib import Path

import scrapy


class Spider(scrapy.Spider):
    name = "newsfeed"

    custom_settings = {
        'LOG_LEVEL': 'WARNING',
    }

    def start_requests(self, **kwargs):
        urlsBBC = [
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

        urlsCNN = [
            'https://edition.cnn.com/',
            'https://edition.cnn.com/sport',
            'https://edition.cnn.com/us',
            'https://edition.cnn.com/world',
            'https://edition.cnn.com/politics',
            'https://edition.cnn.com/business',
            'https://edition.cnn.com/opinions',
            'https://edition.cnn.com/health',
            'https://edition.cnn.com/entertainment',
            'https://edition.cnn.com/style',
            'https://edition.cnn.com/travel'
        ]
        
        for url in urlsBBC:
            yield scrapy.Request(url=url, callback=self.parseBBC)

        for url in urlsCNN:
            yield scrapy.Request(url=url, callback=self.parseCNN)

    def parseBBC(self, response):
        #response.xpath('//a[contains(@data-link-type, "article")]/@href')
        allNews = response.xpath('//div[contains(@class, "module__content")]//ul/li//a[contains(@class, "media__link")]|//div[contains(@id, "site-container")]//a[starts-with(@class, "gs-c-promo-heading")]')
        #for news in allNews:
        #    print("news:::: " + news.get())
        
        for news in allNews:
            link = news.xpath('./@href').get().strip()

            if(link.split("/")[0] != "http" and link.split("/")[0] != "https" and link.split("/")[0] != "https:" and link.split("/")[0] != "http:"):
                link = "https://www.bbc.com" + link

            yield scrapy.Request(url=link, callback=self.parse_article)

    def parseCNN(self, response):
        allNews = response.xpath('//a[contains(@data-link-type, "article")]')
        #for news in allNews:
        #    print("news:::: " + news.get())
        
        for news in allNews:
            link = news.xpath('./@href').get().strip()

            if(link.split("/")[0] != "http" and link.split("/")[0] != "https" and link.split("/")[0] != "https:" and link.split("/")[0] != "http:"):
                link = "https://edition.cnn.com" + link

            yield scrapy.Request(url=link, callback=self.parse_article)

    def parse_article(self, response):
            article = response.xpath('//article//p/text()|//article//p/b/text()|//article//p/span/text()|//div[contains(@class, "BasicArticle__main")]//div/text()|//div[contains(@class, "BasicArticle__main")]//div/a/text()')
            name = response.xpath('//article//h1/text()|//div//h1/text()').get()

            if(name != ""):
                text = ""

                for txt in article:
                    text = text + txt.get().strip()

                
                try:
                    yield self.output_callback({
                        'name': name.strip(),
                        'link': response.request.url,
                        'text': text,
                        'ranking': 1
                    })
                except:
                    print("Empty")

            
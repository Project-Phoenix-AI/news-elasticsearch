import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['http://example.com']

    def parse(self, response):
        # Extract the title and text from the web page
        title = response.css('h1::text').get()
        text = response.css('p::text').getall()

        # Store the extracted data in a dictionary or item
        data = {
            'title': title,
            'text': text
        }

        # Yield the data to be processed further or stored
        yield data

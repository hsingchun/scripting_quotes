import scrapy
import json

class BypageSpider(scrapy.Spider):
    name = 'bypage'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']
    page = 1
    # method 1
    def parse(self, response):
        data = json.loads(response.text)
        for quote in data['quotes']:
            yield {'quote': quote['text']}
        if data['has-text']:
            self.page += 1
            url = f"http://quotes.toscrape.com/api/quotes?page={self.page}"
            yield scrapy.Request(url = url, callback=self.parse)
    #method2

    # or use this: https://michael-shub.github.io/curl2scrapy/
    request = scrapy.Request.from_curl(
        '''
        curl 'http://quotes.toscrape.com/page/1/' \
        -H 'Connection: keep-alive' \
        -H 'Upgrade-Insecure-Requests: 1' \
        -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36' \
        -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
        -H 'Referer: http://quotes.toscrape.com/page/2/' \
        -H 'Accept-Language: en-US,en;q=0.9' \
        -H 'Cookie: session=eyJjc3JmX3Rva2VuIjoiVGZuU3NYcHJMWXVqT3lLYU1lSWRKRFZvY0ZQRWdXbUJ6QWtsYndaaFVpUXh2dFJOQ0hHcSJ9.YUx2Qg.n1sPmgIn_TG8fNLYEOXwwGxuHp8' \
        '''
    )

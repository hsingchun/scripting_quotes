import scrapy
# from scrapy.utils.trackref import get_oldest, iter_all

class QuoteSpider(scrapy.Spider):
    name = 'quote'
    # allowed_domains = ['quotes.toscrape.com/']
    start_urls = ['http://quotes.toscrape.com/tag/humor/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'author': quote.xpath('span/small/text()').get(),
                'text': quote.css('span.text::text').get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

# [r.url for r in iter_all('HtmlResponse')]
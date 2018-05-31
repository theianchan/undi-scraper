import scrapy


class AuthorSpider(scrapy.Spider):
    name = "author"
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        for href in response.css(".author + a::attr(href)"):
            yield response.follow(href, self.parse_author)

        for href in response.css("li.next a::attr(href)"):
            yield response.follow(href, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            "name": extract_with_css("h3.author-title::text"),
            "birthdate": extract_with_css(".author-born-date::text"),
            "bio": extract_with_css(".author-description::text")
        }


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            "http://quotes.toscrape.com/page/1/",
            "http://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").extract_first(),
                "author": quote.css("small.author::text").extract_first(),
                "tags": quote.css("div.tags a.tag::text").extract()
            }

        # next_page = response.css("li.next a::attr(href)").extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        for href in response.css("li.next a::attr(href)"):
            yield response.follow(href, callback=self.parse)

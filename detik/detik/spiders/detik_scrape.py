import scrapy

class PostsSpider(scrapy.Spider):
    name = "detik"
    allowed_urls = ['https://www.detik.com']
    start_urls = [
        'https://news.detik.com/indeks'

    ]

    def parse(self, response):
        for post in response.css('.list-content__item'):
            yield {
                'judul berita': post.css('.media__title a::text').get(),
                'link berita': post.css('.media__title a::attr(href)').get(),
                'gambar': post.css('img ::attr(src)').get(),
            }

            next_page = response.css('div.pagination.text-center.mgt-16.mgb-16 ::attr(href)')[-1].get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
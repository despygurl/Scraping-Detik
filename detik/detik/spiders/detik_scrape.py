import scrapy

class PostsSpider(scrapy.Spider):
    name = "detik"
    allowed_urls = ['https://www.detik.com']
    tanggal = input("Masukkan tanggal (dd): ")
    bulan = input("Masukkan bulan (mm): ")
    tahun = input("Masukkan tahun (yyyy): ")
    start_urls = [
        'https://news.detik.com/indeks?date={0}%2F{1}%2F{2}'.format(bulan, tanggal, tahun)

    ]

    def parse_item(self,response):
        pic = response.css('.detail__media-image img::attr(src)').get()
        if pic is None:
            item = {
                "Judul": response.css('.detail__title::text').get().strip(),
                'Author': response.css('.detail__author::text').get().replace(' - detikNews',''),
                'Topik': response.css('div.nav a::text').getall(),
                'Waktu' : response.css('.detail__date::text').get(),
                'Gambar' : "Gambar tidak tersedia",
                'Isi Berita': "".join(response.css('.detail__body-text.itp_bodycontent p::text').getall())


            }
        else:
            item = {
                "Judul": response.css('.detail__title::text').get().strip(),
                'Author': response.css('.detail__author::text').get().replace(' - detikNews', ''),
                'Topik': response.css('div.nav a::text').getall(),
                'Waktu': response.css('.detail__date::text').get(),
                'Gambar': response.css('.detail__media-image img::attr(src)').get(),
                'Isi Berita': "".join(response.css('.detail__body-text.itp_bodycontent p::text').getall())

            }
        yield item

    def parse(self, response):
        for post in response.css('h3'):
            dict_url = {
                'url': post.css('a::attr(href)').get()
            }
            link = dict_url.get('url')
            if link is not None:
                yield scrapy.Request(url=link, callback=self.parse_item)

            next_page = response.css('div.pagination.text-center.mgt-16.mgb-16 ::attr(href)')[-1].get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
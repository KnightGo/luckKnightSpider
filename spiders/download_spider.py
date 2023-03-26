import scrapy


class DownloadSpider(scrapy.Spider):
    name = "download"

    def start_requests(self):
        urls = [
            'https://www.roxy.com/sale/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
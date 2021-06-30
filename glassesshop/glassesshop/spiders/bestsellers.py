import scrapy


class BestsellersSpider(scrapy.Spider):

    name = "bestsellers"
    allowed_domains = ["www.glassesshop.com"]

    def start_requests(self):

        yield scrapy.Request(
            url="https://www.glassesshop.com/bestsellers",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
            })

    def parse(self, response):

        glasses = response.xpath("//div[contains(@class, 'product-list-item') and not(contains(@class, 'ad-banner'))]")

        for glass in glasses:

            yield {
                "name": glass.xpath(".//div[4]/div[2]/div/div[1]/div/a[contains(@class, 'product') and not(contains(@class, 'none'))]/text()").get().strip(),
                "url": glass.xpath(".//div[4]/div[2]/div/div[1]/div/a[contains(@class, 'product') and not(contains(@class, 'none'))]/@href").get(),
                "price": glass.xpath(".//div[4]/div[2]/div/div[2]/div/div[contains(@class, 'product') and not(contains(@class, 'none'))]/span/text()").get(),
                "img_url": glass.xpath(".//div[3]/a[contains(@class, 'img') and not(contains(@class, 'none'))]/img[contains(@class, 'default')]/@data-src").get()
            }

        next_page = response.xpath("//a[text()='Next']/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
            })

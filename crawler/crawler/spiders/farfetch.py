import scrapy


import scrapy

class FarfetchSpider(scrapy.Spider):
    name = "farfetch"
    allowed_domains = ["www.farfetch.com"]
    start_urls = [
        "https://www.farfetch.com/np/shopping/men/clothing-2/items.aspx",
        "https://www.farfetch.com/np/shopping/men/t-shirts-vests-2/items.aspx",
        "https://www.farfetch.com/np/shopping/men/jackets-2/items.aspx"
                  ]

    def parse(self, response):
        clothes = response.xpath('//div[@data-component="ProductCardImageContainer"]')

        for cloth in clothes:
            item = {}
            # print(cloth)
            # print(cloth.xpath('.//img/@src'))
            image_url = cloth.xpath('.//img/@src').get('image_url')
            if image_url:
                item['image_url'] = image_url
                yield item


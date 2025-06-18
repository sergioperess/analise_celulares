import scrapy


class MagaluSpider(scrapy.Spider):
    name = "magalu"
    allowed_domains = ["www.magazineluiza.com.br"]
    start_urls = ["https://www.magazineluiza.com.br/busca/iphone/"]
    start_page = 1
    max_page = 3

    def parse(self, response):
        
        products = response.css('li.sc-CCtys.fdofhQ')
        
        for product in products:
        
            
            yield{
                'image': product.css('div.sc-bHvAfQ.YCjdw img::attr(src)').get(),
                'name': product.css('h2.sc-dxlmjS.NMyym::text').get(),
                'reviews_rating_number': product.css('span.sc-jwZKMi.ijDyWI::text').get(),
                'old_price': product.css('p.sc-dcJsrY.lmAmKF.sc-cyRcrZ.lvyBD::text').get(default=None),
                'new_price': product.css('p.sc-dcJsrY.eLxcFM.sc-hgRRfv.dfAhbD::text').get(default=None),
            }

        
            if self.start_page < self.max_page:
                next_url = f"https://www.magazineluiza.com.br/busca/iphone/?page={self.start_page}"
                self.start_page += 1
                yield response.follow(next_url, callback=self.parse)
                
        

from scrapy.spiders import Spider
import requests

#Your Spider name
class SpiderName(Spider):
    name = "Name of the scrap"
    allowed_domains = ['Domain to scrap']
    page_number = 1
    start_urls = ['Your URL']

    def parse(self, response):
        # Get href of the products on the page
        for link in response.css('h3.card-information__text a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_variants)

    def parse_variants(self, response):
        # Get the JSON file of each product adding ".js" at the end of each URL
        text = '.js'
        # Get the URL of the product
        url = response.css('link::attr(href)').get() 
        full_url = url + text
        # Get all the variant listed in the JSON
        parsing = requests.get(full_url).json()
        for x in range(0,len(parsing['variants'])):
            yield {
                'added_on_store': parsing['created_at'],
                'type': parsing['type'],
                'brand': parsing['vendor'],
                'product_name': parsing['title'],
                'variant_name': parsing['variants'][x]['title'],
                'current_price': parsing['variants'][x]['price'],
                'original_price': parsing['variants'][x]['compare_at_price'],
                'bar_code/GTIN': parsing['variants'][x]['barcode']
            }
        
        # Go to next page 
        next_page = 'Your URL' + str(SpiderName.page_number)
        # Manually input the number of pages to be scrapped
        if SpiderName.page_number < 4:
            yield response.follow(next_page, callback=self.parse)
            SpiderName.page_number += 1
             
 
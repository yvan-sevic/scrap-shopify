from scrapy.spiders import Spider
import requests
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import scrapy

#Name of your spider
class SpiderName(Spider):
    name = "Project Name"
    allowed_domains = ['Domain name']

    def start_requests(self):
        options = ChromeOptions()
        options.headless = True
        #Path to your chrome driver.exe
        driver = Chrome('C:\\', options=options)
        #Iterate through the number of pages set below
        page_number = 1
        for i in range(page_number):
            url = 'Your URL name' + str(i + 1)
            driver.get(url)
            allContent = driver.find_elements(By.CLASS_NAME,'productitem--image-link')
            #Get all the HREF from the page and yield to each one
            for info in allContent:
                hrefs = info.get_attribute('href')
                yield scrapy.Request(hrefs, callback=self.parse_variants)
        
    #Inside each products
    def parse_variants(self, response):
        #add '.js' to get the JSON 
        text = '.js'
        url = response.xpath('//link[6]/@href').get()
        full_url = url + text
        parsing = requests.get(full_url).json()
        #Loop through all the variants
        for x in range(0,len(parsing['variants'])):
            yield {
                'added_on_store': parsing['created_at'],
                'type': parsing['type'],
                'product_name': parsing['title'],
                'variant_name': parsing['variants'][x]['title'],
                'current_price': parsing['variants'][x]['price'],
                'original_price': parsing['variants'][x]['compare_at_price'],
                'bar_code/GTIN': parsing['variants'][x]['barcode']
            }
        
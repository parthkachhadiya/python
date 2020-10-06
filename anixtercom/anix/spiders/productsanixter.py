# -*- coding: utf-8 -*-
import scrapy
from anix.items import AnixProduct

class ProductsanixterSpider(scrapy.Spider):
    name = 'productsanixter'
    allowed_domains = ['anixter.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'anix.pipelines.AnixterProductPipeline': 100
        }
    }
    
    def start_requests(self):
        self.total_pages = []
        start_urls = [
                      'https://www.anixter.com/en_us/products/Wire-and-Cable/c/CATEGORY_01',
                      'https://www.anixter.com/en_us/products/Communications/c/CATEGORY_02',
                      'https://www.anixter.com/en_us/products/Security/c/CATEGORY_03',
                      'https://www.anixter.com/en_us/products/Networking/c/CATEGORY_04',
                      'https://www.anixter.com/en_us/products/Hardware-and-Supplies/c/CATEGORY_05',
                      'https://www.anixter.com/en_us/products/Industrial-Communication-and-Control/c/CATEGORY_06'
                      ]
        for url in start_urls:
            yield scrapy.Request(url, callback=self.getPageURLs)
        
        # for pagination_url in self.total_pages:
        #     yield scrapy.Request(url=pagination_url, callback=self.parse_pagination_url)
    
    def getText(self, parsed_source, xpath_str):
        try:
            text = parsed_source.xpath(xpath_str).extract()
            if len(text) == 0:
                return ''
            else:
                return text[0].replace('\n','').replace('\t','').replace('\r','').strip()
        except:
            return ""

    # def parse(self, response):
    #     if '/Wire-and-Cable/c/CATEGORY_01' in response.body:
    #         print "category found"
    #     print response.xpath("//a/@href")
    #     cat_urls = response.xpath("//li/a[contains(@href,'/c/CATEGORY_')]/@href").extract()
    #     print "total cat_urls:", cat_urls
    #     for cat_url in cat_urls:
    #         yield scrapy.Request(url=cat_url, callback=self.getPageURLs)
    
    def getPageURLs(self, response):
        cat = response.url
        try:
            product_count = int(self.getText(response,"//div[contains(@class,'result-count')]/span/text()").split('of')[1].strip())
            print "total products in this category", product_count
        except:
            return
        
        if product_count % 20 == 0:
           page_count = product_count / 20
        else:
           page_count = (product_count / 20) + 1
           
        print "Pagination Count :", page_count
        # save_product_urls(parsed_source, cat)
        #if 'https://www.anixter.com/en_us/c/CATEGORY_05' in cat:
        #    page_start = 4487
        #else:
        page_start = 1
        for r in xrange(page_start, page_count+1):
            nextCat = cat + '?q=%3Arelevance&page=' + str(r) + '&op='
            yield scrapy.Request(url=nextCat, callback=self.parse_pagination_url)
            # self.total_pages.append(nextCat)
    
    def parse_pagination_url(self,response):
        all_products = response.xpath("//p[@class='title-primary']/a/@href").extract()
        all_products = [response.urljoin(url) for url in all_products if url.startswith('/')]
        print "added", len(all_products), "to db"
        for product in all_products:
            item = AnixProduct()
            item['product_url'] = product
            item['cat_url'] = ''
            yield item
        
        

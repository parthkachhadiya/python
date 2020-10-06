# -*- coding: utf-8 -*-
import scrapy
import psycopg2
from anix.items import AnixItem
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
class AnixterSpider(scrapy.Spider):
    name = 'anixter'
    allowed_domains = ['anixter.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'anix.pipelines.AnixPipeline': 100
        }
    }
    def start_requests(self):
        hostname = '159.65.xxx.xxx'
        username = 'postgres'
        password = 'xxx@xxxx'
        database = 'xxxxx'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()
        self.cur.execute("select distinct product_url from anixtercom_product_urls vpu left join anixtercom v on vpu.product_url = v.source_url where v.source_url is NULL")
        urls = self.cur.fetchall()
        # print urls[0]
        # urls = [('https://www.anixter.com/en_us/products/001E38-31331-29/CORNING/Indoor-Fiber-Optic-Cable/p/370-COROS2-TBIC20-01',)]
        for url in urls:
            # r = scrapy.Request(url=url[0], callback=self.parse,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'})
            # return [r]
            # print r.headers
            ua = UserAgent()
            user_agent=ua.random
            yield scrapy.Request(url=url[0], callback=self.parse,headers={'User-Agent':user_agent},meta={'url':url[0]})
            # break
            # python2.7 -m scrapy crawl anixter
            # yield scrapy.Request(url=url[0]+'/price?table=false', callback=self.parse,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'})
    
    def getDescription(self, parsed_source, xpath_str):
        try:
            text_list = parsed_source.xpath(xpath_str).extract()
            if len(text_list) == 0:
                return ''
            else:
                text_list = [x.replace('\n','').replace('\t','').replace('\r','').strip() for x in text_list]
                content = " ".join(text_list).strip()
                return content
        except:
            print traceback.format_exc()
            return ''


    def getText(self, parsed_source, xpath_str):
        try:
            text = parsed_source.xpath(xpath_str).extract()
            if len(text) == 0:
                return ''
            else:
                return text[0].replace('\n','').replace('\t','').replace('\r','').strip()
        except:
            return ""


    def getPrice(self, parsed_source, xpath_str):
        text = parsed_source.xpath(xpath_str).extract()
        if len(text) == 0:
            return 0
        else:

            price = re.findall("\d+",text[0].replace(",",""))
            if price:
                return ".".join(price)
            else:
                return ""

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        parsed_source = response
        source_url = response.meta.get('url')
        keys = ['manufacturer','Brand','manufacturer_number','item_number','upc','unspsc','product_name','item_detailed','package_size','Order_Unit',
                'minimum_quantity','Currency_Code','Without_Tax','VAT','msrp_list_price','retail_price_your_price','discount_you_save_amount','discount_you_save_percentage','volume_price_1','volume_for_discount_1','volume_discount_1','volume_price_2','volume_for_discount_2','volume_discount_2','volume_price_3','volume_for_discount_3','volume_discount_3','volume_price_4','volume_for_discount_4','volume_discount_4','volume_price_5','volume_for_discount_5','volume_discount_5','volume_price_6','volume_for_discount_6','volume_discount_6','volume_price_7','volume_for_discount_7','volume_discount_7','volume_price_8','volume_for_discount_8','volume_discount_8','volume_price_9','volume_for_discount_9','volume_discount_9','volume_price_10','volume_for_discount_10','volume_discount_10',
                'product_attributes_technical_specs','features','specification','applications','caution','in_stock','category','sub_category',
                'country_of_origin','catalog','guarantee_information','shipping_information', 'path', 'source_url' , 'cross_referencing_product_url','cross_referencing_product_name', 'private_label']
        item = AnixItem()
        for k in keys:
            item[k] = ''
        item['source_url'] = source_url
        pnfStatus = self.getText(parsed_source, "//div[contains(text(),'This item has been discontinued')]/text()")
        attributeList = []
        #if pnfStatus:
        #    item_number = self.getText(parsed_source, "//div[@class='col-sm-7']/div[2]/span[2]/text()")
        #    manufacturer_number = self.getText(parsed_source, "//div[@class='col-sm-7']/div[1]/span[2]/text()")
        #    in_stock = "Discontinued"       
        if True:
            item['manufacturer'] = self.getText(parsed_source, "//span[@class='inner-product-heading']/b[1]/text()")
            
            item['manufacturer_number'] = self.getText(parsed_source, "//div[@class='col-sm-7']/div[1]/span[2]/text()")  
            
            item['item_number'] = self.getText(parsed_source, "//div[@class='col-sm-7']/div[2]/span[2]/text()")
            
            product_name = self.getDescription(parsed_source, "//meta[@name='description']/@content")
            item['product_name'] = product_name.replace('  ','')
            if product_name == '':
                print "No Product name found"
                return None
            
            item['item_detailed'] = self.getText(parsed_source, "//div[@class='tab-container']/p/text()")

            # price_parse,source = request_parse_source_url(product_url + '/price?table=false',SOURCE_URL,proxy=False)
            #price_parse = get_parsed_source_browser(product_url + '/price?table=false',SOURCE_URL)
            #print self.getText(price_parse, "//div[@class='price']//text()")
            #price = getPrice(parsed_source, "//div[@class='price']/span/em/text()")
            #import ipdb;ipdb.set_trace()
            #print self.getDescription(parsed_source, "//div[@class='price']//text()"), price
            #package_size = self.getText(parsed_source,"//div[@class='product-measurement']/text()").replace('/','')
            
            if 'Specification' in self.getText(parsed_source, "//*[@id='fragment-1']/div[1]/div[1]/h3[1]/text()"):
                item['specification'] = self.getDescription(parsed_source, "//*[@id='fragment-1']/div[1]/div[1]/p[1]/text()")
            if 'Specification' in self.getText(parsed_source, "//*[@id='fragment-1']/div[1]/div[1]/h3[2]/text()") or 'Specification' in self.getText(parsed_source, "//*[@id='fragment-1']/div[1]/div[1]/h3[3]/text()"):
                item['specification'] = self.getDescription(parsed_source, "//*[@id='fragment-1']/div[1]/div[1]/p[2]/text()")
            try:
                if item['specification']=='':
                    if 'Specification' in self.getText(parsed_source, "//*[@class='productFeatureClasses']/div[1]/h3[1]/text()"):
                        item['specification'] = self.getDescription(parsed_source, "//*[@class='productFeatureClasses']/div[2]/text()")
            except:
                pass
            
            item['features'] = self.getDescription(parsed_source, "//div[@class='toggle-content short-text']/ul//text()")
            item['applications']=''
            if 'Applications' in self.getText(parsed_source, "//div[@class='toggle-content short-text']/h3/text()"):
                item['applications'] = self.getText(parsed_source, "//div[@class='toggle-content short-text']/p/text()")
            print("item['applications']=================>>>",item['applications'])
            i = 0        
            spec_rows = parsed_source.xpath("//div[@class='spec-listing']/table/tbody/tr")
            
            tech_info = self.getText(parsed_source, "//h3[text()='Tech Info']/following-sibling::p/text()")
            #print "tech_info :", tech_info
            attributeList = []
            if tech_info: 
                attributeList.append('Tech Info')
                attributeList.append(tech_info)
                
            if parsed_source.xpath("//*[@title='References']"):
                print("hello here")
                #attType = self.getDescription(parsed_source,"//div[@id='prodReferences']//text()")
                # attType = self.getDescription(parsed_source,"//div[@id='prodReferences']/a//text()")
                # attVal = self.getDescription(parsed_source,"//div[@id='prodReferences']/a//@href")
                attType = parsed_source.xpath("//div[@id='prodReferences']/a//text()").extract()
                attVal = parsed_source.xpath("//div[@id='prodReferences']/a//@href").extract()
                print(type(attType))
                print(type(attVal))
                #print attType, ":", attVal
                # attributeList.append(attType)
                # attributeList.append(attVal)
                for index,row in enumerate(attType):
                    attributeList.append(attType[index])
                    attributeList.append(attVal[index])
            # print("attType",attType)
            # print("attVAl",attVal)    
            
            
            for row in spec_rows:
                typeX = self.getText(row, "./td[1]/span/text()")
                value = self.getText(row, "./td[2]/span/text()")
                print i, typeX, value, '*'*49
                if 'UNSPSC' in typeX: 
                    item['unspsc'] = value
                    #print "unspsc :", unspsc
                if len(typeX) > 498 and len(value) < 2:
                    typeX = typeX[:497]
                    value = typeX[497:]
                if spec_rows[0]==row:
                    item['product_attributes_technical_specs'] += ' ' + typeX + ':' + value
                elif spec_rows[0]==row:
                    item['product_attributes_technical_specs'] += '; ' + typeX + ':' + value
                else:
                    item['product_attributes_technical_specs'] += '; ' + typeX + ':' + value
                attributeList.extend([typeX, value])
                i += 2
            item['product_attributes_technical_specs'] = item['product_attributes_technical_specs'].strip()
            print("product_attributes_technical_specs===========",item['product_attributes_technical_specs'])
            if len(item['product_attributes_technical_specs']) > 4999 : item['product_attributes_technical_specs'] = item['product_attributes_technical_specs'][:4998]
            j = 0  
            if pnfStatus:
                in_stock = "Discontinued"
                if in_stock == '':
                    in_stock = "N/A"
            else:
                in_stock = self.getDescription(parsed_source,"//div[@class='product-shipping']//text()").strip()
                if 'in stock' in in_stock.lower():
                    in_stock = 'In stock'
                else:
                    in_stock = 'N/A'
            
            print "in_stock :", in_stock
            item['in_stock'] = in_stock
            
            breadcrumbs = parsed_source.xpath("//div[@id='breadcrumb']//text()").extract()
            breadcrumbs = [x.replace('\n', '').replace('\t','').strip() for x in breadcrumbs]
            breadcrumbs[:] = [t for t in breadcrumbs if t != '']
            item['path'] = ((' / '.join(breadcrumbs)).replace('&#47;', '').strip()).replace('/',' ').replace('  ','')
            print item['path']
            
            if len(breadcrumbs) > 10:
                item['category'] = breadcrumbs[4]
                item['sub_category'] = breadcrumbs[6]
            
            item['catalog'] = self.getText(parsed_source, "//div[@class='col-xs-5 col-sm-4']/a/@href|//div[@class='col-xs-4 col-sm-2']/a/@href")  
            item['minimum_quantity'] = self.getText(parsed_source, "//div[@class='minimum']/text()")
            item['shipping_information'] = self.getDescription(parsed_source, "//div[h3[text()='Shipping and Fulfillment Policy']]/p//text()").encode('utf-8','ignore')

            if len(attributeList) > 100: 
                attributeList = attributeList[:100]
            elif len(attributeList) < 100:
                for k in range(len(attributeList), 100):
                    attributeList.append('')
            attr_count = 1
            for attr_type, attr_val in zip([z for i,z in enumerate(attributeList) if i%2==0], [z for i,z in enumerate(attributeList) if i%2==1]):
                item['attribute_type_'+str(attr_count)] = attr_type
                item['attribute_value_'+str(attr_count)] = attr_val
                attr_count += 1
            req = scrapy.Request(url=source_url+'/price?table=false',callback=self.parse2, meta={'item':item})
            return req 
            """
            req = scrapy.Request(url=source_url+'/price?table=false')
            print dir(req)
            price_parse = req.response
            if 'Discontinued Item' in price_parse.body:
                price='0'
                guarantee_information = 'Discontinued Item'
            else:
                price = self.getPrice(price_parse, "//div[@class='price']/span/em/text()")
                guarantee_information = self.getDescription(price_parse, "//div[@class='price']//text()")
            print 'price_text:',guarantee_information,'price:', price
            item['msrp_list_price'] = price
            item['guarantee_information'] = guarantee_information
            package_size = self.getText(price_parse,"//div[@class='product-measurement']/text()").replace('/','')
            #item = reponse.meta['item']
            print item
            #item['price'] = price
            return item
            """


    def parse2(self,response):
        price_parse = response
        item = response.meta['item']
        #item = AnixItem()
        if 'Discontinued Item' in price_parse.body:
            price='0'
            guarantee_information = 'Discontinued Item'
        else:
            price = self.getPrice(price_parse, "//div[@class='price']/span/em/text()")
            guarantee_information = self.getDescription(price_parse, "//div[@class='price']//text()")
        print 'price_text:',guarantee_information,'price:', price
        #item['source_url'] = response.url
        #item['msrp_list_price'] = str(price)
        item['retail_price_your_price'] = str(price)
       
        item['guarantee_information'] = guarantee_information.replace('$','').replace(str(price),'').strip()

        item['package_size'] = self.getText(price_parse,"//div[@class='product-measurement']/text()").replace('/','')
        # return item
        yield item

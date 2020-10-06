# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
import traceback
from psycopg2 import IntegrityError
import logging

class AnixterProductPipeline(object):
    def open_spider(self, spider):
        hostname = '159.65.xxx.xx'
        username = 'postgres'
        password = 'xxxx@xxxxx'
        database = 'xxxxxxxxxxxx'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS anixtercom_product_urls
                (
                  id serial,
                  product_url character varying(400),
                  cat_url character varying(400)
                )""")
        
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS anixtercom
                    (
                      id serial,
                      manufacturer character varying(1000),
                      Brand character varying(1000),
                      manufacturer_number character varying(1000),
                      item_number character varying(1000),
                      upc character varying(1000), 
                      unspsc character varying(1000), 
                      product_name character varying(1000),
                      item_detailed character varying(3000), 
                      package_size character varying(100),
                      Order_Unit  character varying(1000),
                      minimum_quantity character varying(100), 
                      Currency_Code character varying(1000),
                      Without_Tax character varying(1000),
                      VAT character varying(1000),
                      msrp_list_price character varying(100),
                      retail_price_your_price character varying(100),
                      discount_you_save_amount character varying(100),
                      discount_you_save_percentage character varying(100),
                      volume_price_1 character varying(1000),
                        volume_for_discount_1 character varying(1000),
                        volume_discount_1 character varying(1000),
                        volume_price_2 character varying(1000),
                        volume_for_discount_2 character varying(1000),
                        volume_discount_2 character varying(1000),
                        volume_price_3 character varying(1000),
                        volume_for_discount_3 character varying(1000),
                        volume_discount_3 character varying(1000),
                        volume_price_4 character varying(1000),
                        volume_for_discount_4 character varying(1000),
                        volume_discount_4 character varying(1000),
                        volume_price_5 character varying(1000),
                        volume_for_discount_5 character varying(1000),
                        volume_discount_5 character varying(1000),
                        volume_price_6 character varying(1000),
                        volume_for_discount_6 character varying(1000),
                        volume_discount_6 character varying(1000),
                        volume_price_7 character varying(1000),
                        volume_for_discount_7 character varying(1000),
                        volume_discount_7 character varying(1000),
                        volume_price_8 character varying(1000),
                        volume_for_discount_8 character varying(1000),
                        volume_discount_8 character varying(1000),
                        volume_price_9 character varying(1000),
                        volume_for_discount_9 character varying(1000),
                        volume_discount_9 character varying(1000),
                        volume_price_10 character varying(1000),
                        volume_for_discount_10 character varying(1000),
                        volume_discount_10 character varying(1000),
                      product_attributes_technical_specs character varying(5000),
                      features character varying(5000), 
                      specification character varying(1500), 
                      applications character varying(1500), 
                      caution character varying(1500), 
                      in_stock character varying(100),
                      category character varying(100),
                      sub_category character varying(100),
                      country_of_origin character varying(100),
                      catalog character varying(500),
                      guarantee_information character varying(5000), 
                      shipping_information character varying(5000), 
                      path character varying(500),
                      source_url character varying(500) UNIQUE,
                      cross_referencing_product_url character varying(5000),
                      cross_referencing_product_name character varying(5000),
                      private_label character varying(20)
                    )
                    WITH (
                      OIDS=FALSE
                    )
                """)
        self.connection.commit()
        for i in range(1,51):
            try:
                q = "alter table anixtercom add column attribute_type_"+str(i)+" character varying(1000)"
                self.cur.execute(q)
                q = "alter table anixtercom add column attribute_value_"+str(i)+" character varying(1000)"
                self.cur.execute(q)
                self.connection.commit()
            except:
                print traceback.print_exc()
                self.connection.rollback()
        #self.connection.commit()
    
    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
   
    def __repr__(self):
        return "done: "+item['product_url']

    def process_item(self, item, spider):
        try:
            q = "insert into anixtercom_product_urls values (DEFAULT,%s,%s)"
            print q
            self.cur.execute(q, (item['product_url'], item['cat_url']))
            self.connection.commit()
            print "saved to db"
        except:
            print traceback.print_exc()

class AnixPipeline(object):
    def open_spider(self, spider):
        hostname = '159.65.160.78'
        username = 'postgres'
        password = 'KenAr@2018'
        database = 'industryparts'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()
        self.keys = ['manufacturer','Brand','manufacturer_number','item_number','upc','unspsc','product_name','item_detailed','package_size','Order_Unit',
                'minimum_quantity','Currency_Code','Without_Tax','VAT','msrp_list_price','retail_price_your_price','discount_you_save_amount','discount_you_save_percentage',
                'volume_price_1','volume_for_discount_1','volume_discount_1','volume_price_2','volume_for_discount_2','volume_discount_2','volume_price_3',
                'volume_for_discount_3','volume_discount_3','volume_price_4','volume_for_discount_4','volume_discount_4','volume_price_5',
                'volume_for_discount_5','volume_discount_5','volume_price_6','volume_for_discount_6','volume_discount_6','volume_price_7',
                'volume_for_discount_7','volume_discount_7','volume_price_8','volume_for_discount_8','volume_discount_8','volume_price_9',
                'volume_for_discount_9','volume_discount_9','volume_price_10','volume_for_discount_10','volume_discount_10',
                'product_attributes_technical_specs','features','specification','applications','caution','in_stock','category','sub_category',
                'country_of_origin','catalog','guarantee_information','shipping_information', 'path' ,'source_url' ,'cross_referencing_product_url','cross_referencing_product_name', 'private_label']
        for k in range(1,51):
            self.keys.append('attribute_type_'+str(k))
            self.keys.append('attribute_value_'+str(k))
        self.logger = logging.getLogger()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        try:
            print item['source_url']
            if '/price' in item['source_url']:
                q = "update anixtercom set msrp_list_price=%s,guarantee_information=%s,package_size=%s where source_url=%s"
                print q
                self.cur.execute(q,(item['msrp_list_price'],item['guarantee_information'],item['package_size'],item['source_url'].split('/price')[0]))
                self.connection.commit()
            else:
                q = "insert into anixtercom values (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                #print q
                data = []
                for k in self.keys:
                    try:
                        text = item[k].encode('ascii',errors='ignore').decode('utf-8',errors='ignore')
                    except:
                        text = item[k].decode('ascii',errors='ignore').encode('utf-8',errors='ignore')
                    #data.append(item[k].encode('ascii',errors='ignore').decode('utf-8',errors='ignore'))
                    data.append(str(text))
                    
                #data = [item[k].decode('ascii','ignore').encode('utf8','ignore') for k in self.keys]
                #print data
                #print "**********************************************data", len(data)
                try:
                    self.cur.execute(q,data)
                    self.connection.commit()
                    self.logger.info("*********************saved data to db*******************************")
                except IntegrityError as ie:
                    self.logger.error(traceback.print_exc())
                    self.connection.rollback()
                    print "URL already exist. Not adding this", item.get(['source_url'])
                except:
                    self.logger.error(traceback.print_exc())
                    self.connection.rollback()

            
        except:
            print traceback.print_exc()
        return item
    #def process_item(self, item, spider):
    #    return item

"""
class AnixPipeline(object):
    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'postgres'
        password = 'postgres'
        database = 'industryparts'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        q = ""
        self.cur.execute(q,())
        self.connection.commit()
        return item
    #def process_item(self, item, spider):
    #    return item
"""

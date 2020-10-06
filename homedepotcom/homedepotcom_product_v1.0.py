import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import IntegrityError
import json
import time
import datetime
import random
#import mysql.connector
import sender
from scrapy.http import HtmlResponse
from random import randint
import pprint
import re
import traceback
import math,csv
import certifi
not_av=[]
conn = psycopg2.connect("dbname='xxxxx' user='postgres' host='159.65.xxx.xx' password='xxxx@2018'")
cur = conn.cursor()

TABLE_NAME = "homedepot"

cur.execute(""" CREATE TABLE IF NOT EXISTS %s_product_urls
                (
                  id serial,
                  product_url text primary key,
                  scraped boolean
                )"""%TABLE_NAME)
conn.commit() 

cur.execute("""CREATE TABLE IF NOT EXISTS %s
                (
                        id serial,
                        Source_Website text,
                        manufacturer character varying(5000),
                        Brand character varying(1000),
                        manufacturer_number character varying(5000),
                        item_number character varying(5000),
                        upc character varying(1000),
                        unspsc character varying(1000),
                        product_name character varying(1000),
                        item_detailed character varying(2000),
                        package_size character varying(1000),
                        Order_Unit  character varying(1000),
                        minimum_quantity character varying(1000),
                        Currency_Code character varying(1000),
                        Without_Tax character varying(1000),
                        VAT character varying(1000),
                        msrp_list_price character varying(1000),
                        retail_price_your_price character varying(1000),
                        discount_you_save_amount character varying(1000),
                        discount_you_save_percentage character varying(1000),
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
                        specification character varying(5000),
                        applications character varying(5000),
                        caution character varying(2500),
                        in_stock character varying(1000),
                        category character varying(1000),
                        sub_category character varying(1000),
                        country_of_origin character varying(1000),
                        catalog character varying(1000),
                        guarantee_information character varying(5000),
                        shipping_information character varying(5000),
                        path character varying(5000),
                        source_url character varying(5000),
                        cross_referencing_product_url character varying(5000),
                        cross_referencing_product_name character varying(5000),
                        private_label character varying(20),
                        attribute_type_1 character varying(5000),
                        attribute_value_1 character varying(5000),
                        attribute_type_2 character varying(5000),
                        attribute_value_2 character varying(5000),
                        attribute_type_3 character varying(5000),
                        attribute_value_3 character varying(5000),
                        attribute_type_4 character varying(5000),
                        attribute_value_4 character varying(5000),
                        attribute_type_5 character varying(5000),
                        attribute_value_5 character varying(5000),
                        attribute_type_6 character varying(5000),
                        attribute_value_6 character varying(5000),
                        attribute_type_7 character varying(5000),
                        attribute_value_7 character varying(5000),
                        attribute_type_8 character varying(5000),
                        attribute_value_8 character varying(5000),
                        attribute_type_9 character varying(5000),
                        attribute_value_9 character varying(5000),
                        attribute_type_10 character varying(5000),
                        attribute_value_10 character varying(5000),
                        attribute_type_11 character varying(5000),
                        attribute_value_11 character varying(5000),
                        attribute_type_12 character varying(5000),
                        attribute_value_12 character varying(5000),
                        attribute_type_13 character varying(5000),
                        attribute_value_13 character varying(5000),
                        attribute_type_14 character varying(5000),
                        attribute_value_14 character varying(5000),
                        attribute_type_15 character varying(5000),
                        attribute_value_15 character varying(5000),
                        attribute_type_16 character varying(5000),
                        attribute_value_16 character varying(5000),
                        attribute_type_17 character varying(5000),
                        attribute_value_17 character varying(5000),
                        attribute_type_18 character varying(5000),
                        attribute_value_18 character varying(5000),
                        attribute_type_19 character varying(5000),
                        attribute_value_19 character varying(5000),
                        attribute_type_20 character varying(5000),
                        attribute_value_20 character varying(5000),
                        attribute_type_21 character varying(5000),
                        attribute_value_21 character varying(5000),
                        attribute_type_22 character varying(5000),
                        attribute_value_22 character varying(5000),
                        attribute_type_23 character varying(5000),
                        attribute_value_23 character varying(5000),
                        attribute_type_24 character varying(5000),
                        attribute_value_24 character varying(5000),
                        attribute_type_25 character varying(5000),
                        attribute_value_25 character varying(5000),
                        attribute_type_26 character varying(5000),
                        attribute_value_26 character varying(5000),
                        attribute_type_27 character varying(5000),
                        attribute_value_27 character varying(5000),
                        attribute_type_28 character varying(5000),
                        attribute_value_28 character varying(5000),
                        attribute_type_29 character varying(5000),
                        attribute_value_29 character varying(5000),
                        attribute_type_30 character varying(5000),
                        attribute_value_30 character varying(5000),
                        attribute_type_31 character varying(5000),
                        attribute_value_31 character varying(5000),
                        attribute_type_32 character varying(5000),
                        attribute_value_32 character varying(5000),
                        attribute_type_33 character varying(5000),
                        attribute_value_33 character varying(5000),
                        attribute_type_34 character varying(5000),
                        attribute_value_34 character varying(5000),
                        attribute_type_35 character varying(5000),
                        attribute_value_35 character varying(5000),
                        attribute_type_36 character varying(5000),
                        attribute_value_36 character varying(5000),
                        attribute_type_37 character varying(5000),
                        attribute_value_37 character varying(5000),
                        attribute_type_38 character varying(5000),
                        attribute_value_38 character varying(5000),
                        attribute_type_39 character varying(5000),
                        attribute_value_39 character varying(5000),
                        attribute_type_40 character varying(5000),
                        attribute_value_40 character varying(5000),
                        attribute_type_41 character varying(5000),
                        attribute_value_41 character varying(5000),
                        attribute_type_42 character varying(5000),
                        attribute_value_42 character varying(5000),
                        attribute_type_43 character varying(5000),
                        attribute_value_43 character varying(5000),
                        attribute_type_44 character varying(5000),
                        attribute_value_44 character varying(5000),
                        attribute_type_45 character varying(5000),
                        attribute_value_45 character varying(5000),
                        attribute_type_46 character varying(5000),
                        attribute_value_46 character varying(5000),
                        attribute_type_47 character varying(5000),
                        attribute_value_47 character varying(5000),
                        attribute_type_48 character varying(5000),
                        attribute_value_48 character varying(5000),
                        attribute_type_49 character varying(5000),
                        attribute_value_49 character varying(5000),
                        attribute_type_50 character varying(5000),
                        attribute_value_50 character varying(5000)
                      
                    )
                    WITH (
                      OIDS=FALSE
                    )"""%TABLE_NAME)

conn.commit() 

def scrap_base_page():
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
        }
    session=requests.session()
    response = session.get("https://www.homedepot.com/sitemap/d/pip_sitemap.xml",headers=headers)
    soup = BeautifulSoup(response.text,"lxml")
    prod_links = soup.findAll("loc")
    for prod in prod_links[::-1]:
        req_pro = prod.text
        url = req_pro.replace("\ufeff","")
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
            }
        session=requests.session()
        response = session.get(url,headers=headers)
        soup = BeautifulSoup(response.text,"lxml")
        prod_link = soup.findAll("loc")
        print(len(prod_link))
        for product in prod_link:
            if '/p/' in product.text:
                print(product.text)
                column = [product.text,False]
                try:
                    conn = psycopg2.connect("dbname='industryparts' user='postgres' host='159.xxx.160.xx' password='xxxxx@2018'")
                    cur = conn.cursor()
                    cur.execute("insert into "+TABLE_NAME+"_product_urls values (DEFAULT, %s,%s)",column)
                    conn.commit()
                    conn.close()
                except IntegrityError:
                    print("Record already exist")
                    conn.rollback()
                except:
                    conn.rollback()
                finally:
                    conn.close()
                    column = []
        # conn = psycopg2.connect("dbname='industryparts_additional' user='postgres' host='159.xx.xx.xxx' password='xxxx@2018'")
        # cur = conn.cursor()            
        # cur.execute("update "+TABLE_NAME+"_xml_urls set scraped=%s where product_url=%s",(True,url))
        # conn.commit()
        # conn.close()            


        




        

if __name__ == "__main__":
    scrap_base_page()
  


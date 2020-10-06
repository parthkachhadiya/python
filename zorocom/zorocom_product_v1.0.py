import psycopg2
from psycopg2.extras import DictCursor
from utils import *
import random,time, urllib
from selenium import webdriver
# from pyvirtualdisplay import Display
import traceback
import json
import logging
import datetime
import sys
from multiprocessing import Process

import xml.etree.ElementTree as ET
import gzip
from StringIO import StringIO
from xml.dom import minidom

'''
python getproducts_zoro.py param1 param2
if param1 is true then script start to capture all cat urls and put them into a txt file
	after that it is read and capturing of URL starts
    if false: just start scraping product URLs saved in depth_cats from index (params2)

'''
logger = logging.getLogger()
logger.setLevel(logging.INFO)
today_string = datetime.datetime.today().strftime("%d%M%Y")
LOG_FILENAME = 'zoro_product_collection_'+datetime.datetime.today().strftime("%d%m%Y")+'.log'
fh = logging.FileHandler(LOG_FILENAME)
fh.setLevel(logging.INFO)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter to ch, fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
logger.addHandler(fh)


# display = Display(visible=0, size=(1366,768))
# display.start()
conn = psycopg2.connect("dbname='industryparts' user='postgres' host='159.65.xxx.xxx' password='xxx@2018'")
# conn = psycopg2.connect("dbname='Ind_test' user='postgres' host='167.99.xxx.xxx' password='xxxx@123'")
cur = conn.cursor(cursor_factory=DictCursor)

all_products_landing_cat = []
already_accessed_category = {}

SOURCE_URL = "https://www.zoro.com"
TABLE_NAME = "zorocom"

cur.execute("""CREATE TABLE IF NOT EXISTS %s
                (
                      id serial,
                        manufacturer character varying(5000),
                        Brand character varying(1000),
                        manufacturer_number character varying(5000),
                        item_number character varying(5000),
                        upc character varying(1000),
                        unspsc character varying(1000),
                        product_name character varying(1000),
                        item_detailed character varying(10000),
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

                    
cur.execute(""" CREATE TABLE IF NOT EXISTS %s_product_urls
                (
                  id serial,
                  product_url character varying(400),
                  cat_url character varying(400),
                  scraped integer
                )"""%TABLE_NAME)

conn.commit()

for ii in range(1,51):
    query1 =  "ALTER TABLE " + TABLE_NAME + " ADD COLUMN " + 'attribute_type_' + str(ii) + " character varying(5000)"
    query2 =  "ALTER TABLE " + TABLE_NAME + " ADD COLUMN " + 'attribute_value_' + str(ii) + " character varying(5000)"
    try:
        cur.execute(query1)
        cur.execute(query2)
        conn.commit()
    except:
        pass
            
conn.commit()
total_cats = []
# browser = webdriver.Firefox()

def url_xml(html_source, child_tag):
    lst = []
    xmldoc = minidom.parseString(html_source)
    obs_values = xmldoc.getElementsByTagName(child_tag)
    for i ,ii in enumerate(obs_values):
        lst.append(obs_values[i].firstChild.nodeValue)
    return lst

base_sitemap_link = "https://www.zoro.com/sitemaps/usa/sitemap-index.xml"
xml_source = request_html_source_url(base_sitemap_link)
#sitemap_page_source = request_parse_source_url(base_prod_link, SOURCE_URL)
tree = ET.fromstring(xml_source)
for children in tree:
    for grandchildren in children:
        if 'loc' in grandchildren.tag and '/sitemap-product-' in grandchildren.text:
            #count += 1
            sitemap_gz = grandchildren.text
            r = requests.get(sitemap_gz)
            sitemap = gzip.GzipFile(fileobj=StringIO(r.content)).read()
            xmlList2 = url_xml(sitemap, 'loc')
            xmlList2 = [u for u in xmlList2 if '/i/' in u]
            try:
                print  sitemap_gz, len(xmlList2), "Product url found"
                print("11")
                for prod in xmlList2:
                    print("prod----",prod)
                    cur.execute("insert into "+TABLE_NAME+"_product_urls (id,cat_url,product_url,scraped) values (DEFAULT, %s, %s, 0)", ('',prod))
                    conn.commit()
                    print("successfull")
            except Exception as e:
                print("e-----------",e)


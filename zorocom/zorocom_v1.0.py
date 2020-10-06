from urllib.request import Request, urlopen, urljoin, URLError
from urllib.parse import urlparse
import ssl,requests,json,time,csv,random
import re
from bs4 import BeautifulSoup
import threading
import urllib
from urllib.request import Request, urlopen, urljoin, URLError
from urllib.parse import urlparse
import queue
import traceback
import sys
from fake_useragent import UserAgent
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import IntegrityError
from multiprocessing import Process, Pool
import random
import json
import os
from scrapy.http import HtmlResponse



dbname="industryparts"
# dbname="Ind_test"
user="postgres"
# host="xxx.xxx.xx.xxx"
# password="xxx@123"
host="159.65.xx.xx"
password="xxxxxxx@2018"

ua = UserAgent()
TABLE_NAME = "zorocom"

core_count=os.cpu_count()
print("Total CPU Core Available: {}".format(core_count))
print("No. of workers: {}".format(int(core_count)+7))

conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname,user,host,password))
cur = conn.cursor(cursor_factory=DictCursor)
cur.execute("""CREATE TABLE IF NOT EXISTS %s( id serial, Source_Website text, manufacturer text, manufacturer_number text, item_number text, upc text, unspsc text, product_name text, item_detailed text, package_size text, minimum_quantity text, Currency_Code text, Without_Tax text, VAT text, msrp_list_price text, retail_price_your_price text, get_this_price text, discount_you_save_amount text, discount_you_save_percentage text, volume_price_1 text, volume_for_discount_1 text, volume_discount_1 text, volume_price_2 text, volume_for_discount_2 text, volume_discount_2 text, volume_price_3 text, volume_for_discount_3 text, volume_discount_3 text, volume_price_4 text, volume_for_discount_4 text, volume_discount_4 text, volume_price_5 text, volume_for_discount_5 text, volume_discount_5 text, volume_price_6 text, volume_for_discount_6 text, volume_discount_6 text, volume_price_7 text, volume_for_discount_7 text, volume_discount_7 text, volume_price_8 text, volume_for_discount_8 text, volume_discount_8 text, volume_price_9 text, volume_for_discount_9 text, volume_discount_9 text, volume_price_10 text, volume_for_discount_10 text, volume_discount_10 text, attributes_technical_specs text, features text, specification text, applications text, caution text, in_stock text, category text, sub_category text, country_of_origin text, catalog text, guarantee_information text, shipping_information text, path text, source_url text, attribute_type_1 text, attribute_value_1 text, attribute_type_2 text, attribute_value_2 text, attribute_type_3 text, attribute_value_3 text, attribute_type_4 text, attribute_value_4 text, attribute_type_5 text, attribute_value_5 text, attribute_type_6 text, attribute_value_6 text, attribute_type_7 text, attribute_value_7 text, attribute_type_8 text, attribute_value_8 text, attribute_type_9 text, attribute_value_9 text, attribute_type_10 text, attribute_value_10 text, attribute_type_11 text, attribute_value_11 text, attribute_type_12 text, attribute_value_12 text, attribute_type_13 text, attribute_value_13 text, attribute_type_14 text, attribute_value_14 text, attribute_type_15 text, attribute_value_15 text, attribute_type_16 text, attribute_value_16 text, attribute_type_17 text, attribute_value_17 text, attribute_type_18 text, attribute_value_18 text, attribute_type_19 text, attribute_value_19 text, attribute_type_20 text, attribute_value_20 text, attribute_type_21 text, attribute_value_21 text, attribute_type_22 text, attribute_value_22 text, attribute_type_23 text, attribute_value_23 text, attribute_type_24 text, attribute_value_24 text, attribute_type_25 text, attribute_value_25 text, attribute_type_26 text, attribute_value_26 text, attribute_type_27 text, attribute_value_27 text, attribute_type_28 text, attribute_value_28 text, attribute_type_29 text, attribute_value_29 text, attribute_type_30 text, attribute_value_30 text, attribute_type_31 text, attribute_value_31 text, attribute_type_32 text, attribute_value_32 text, attribute_type_33 text, attribute_value_33 text, attribute_type_34 text, attribute_value_34 text, attribute_type_35 text, attribute_value_35 text, attribute_type_36 text, attribute_value_36 text, attribute_type_37 text, attribute_value_37 text, attribute_type_38 text, attribute_value_38 text, attribute_type_39 text, attribute_value_39 text, attribute_type_40 text, attribute_value_40 text, attribute_type_41 text, attribute_value_41 text, attribute_type_42 text, attribute_value_42 text, attribute_type_43 text, attribute_value_43 text, attribute_type_44 text, attribute_value_44 text, attribute_type_45 text, attribute_value_45 text, attribute_type_46 text, attribute_value_46 text, attribute_type_47 text, attribute_value_47 text, attribute_type_48 text, attribute_value_48 text, attribute_type_49 text, attribute_value_49 text, attribute_type_50 text, attribute_value_50 text) WITH (OIDS=FALSE)"""%TABLE_NAME)
conn.commit() 
conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname,user,host,password))
cur = conn.cursor(cursor_factory=DictCursor)

headers={
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"

}

def get_page_response(url,postmethod,data):
        Flag=True
        while Flag:
            try:
                session=requests.session()
                if postmethod == "get":
                        response=session.get(url, headers=headers)
                if postmethod == "post":
                        response=session.post(url, headers=headers,data=data)
                if response.status_code == 200 or response.status_code == 404:
                    Flag=False
            except:
                pass
        return response
    
def get_data(urls):
      for link in urls:
        # print("raw_url====",url)
        url=link[0]
        # print("URL========",url)
#   url = "https://www.zoro.com/3m-label-5-in-redwhite-250-labelsroll-54917/i/G5254837/"

        manufacturer=manufacturer_number=item_number=UPC=unspsc=product_name=item_detailed=Package_Size=minimum_quantity=currency_code=without_tax=vat=msrp_list_price=retail_price_your_price=get_this_price=discount_you_save_amount=discount_you_save_percentage=attributes_technical_specs=features=specification=applications=caution=in_stock=category=sub_category=country_of_origin=catalog=guarantee_information=shipping_information=path=source_url=""
        Source_Website=Manufacturer=Manufacturer_Number=Item_Number=UNSPSC=Product_Name=Product_details=Quantity=Specification=Application=Category=Country_of_Origin=Catelog=''
        Source_Website=Manufacturer=Manufacturer_Number=Item_Number=UNSPSC=Product_Name=Item_Detailed=MSRP_Price=attributes_Technical_Specs=Stock=Category=Sub_Category=Shipping_Information=path=Source_url=Currency_Code=""
        Guarantee_Information=c_code=Features=Source_Website=Discount=DisP=Manufacturer=Item_Number=Product_Name=Item_Detailed=Package_Size=Minimum_Quantity=MSRP_Price=Retail=Stock=Category=Sub_Category=Catalog=Shipping_Information=path=Source_url=C_code=""
        globals()['attribute_type_1']=globals()['attribute_value_1']=globals()['attribute_type_2']=globals()['attribute_value_2']=globals()['attribute_type_3']=globals()['attribute_value_3']=globals()['attribute_type_4']=globals()['attribute_value_4']=globals()['attribute_type_5']=globals()['attribute_value_5']=globals()['attribute_type_6']=globals()['attribute_value_6']=globals()['attribute_type_7']=globals()['attribute_value_7']=globals()['attribute_type_8']=globals()['attribute_value_8']=globals()['attribute_type_9']=globals()['attribute_value_9']=globals()['attribute_type_10']=globals()['attribute_value_10']=globals()['attribute_type_11']=globals()['attribute_value_11']=globals()['attribute_type_12']=globals()['attribute_value_12']=globals()['attribute_type_13']=globals()['attribute_value_13']=globals()['attribute_type_14']=globals()['attribute_value_14']=globals()['attribute_type_15']=globals()['attribute_value_15']=globals()['attribute_type_16']=globals()['attribute_value_16']=globals()['attribute_type_17']=globals()['attribute_value_17']=globals()['attribute_type_18']=globals()['attribute_value_18']=globals()['attribute_type_19']=globals()['attribute_value_19']=globals()['attribute_type_20']=globals()['attribute_value_20']=globals()['attribute_type_21']=globals()['attribute_value_21']=globals()['attribute_type_22']=globals()['attribute_value_22']=globals()['attribute_type_23']=globals()['attribute_value_23']=globals()['attribute_type_24']=globals()['attribute_value_24']=globals()['attribute_type_25']=globals()['attribute_value_25']=globals()['attribute_type_26']=globals()['attribute_value_26']=globals()['attribute_type_27']=globals()['attribute_value_27']=globals()['attribute_type_28']=globals()['attribute_value_28']=globals()['attribute_type_29']=globals()['attribute_value_29']=globals()['attribute_type_30']=globals()['attribute_value_30']=globals()['attribute_type_31']=globals()['attribute_value_31']=globals()['attribute_type_32']=globals()['attribute_value_32']=globals()['attribute_type_33']=globals()['attribute_value_33']=globals()['attribute_type_34']=globals()['attribute_value_34']=globals()['attribute_type_35']=globals()['attribute_value_35']=globals()['attribute_type_36']=globals()['attribute_value_36']=globals()['attribute_type_37']=globals()['attribute_value_37']=globals()['attribute_type_38']=globals()['attribute_value_38']=globals()['attribute_type_39']=globals()['attribute_value_39']=globals()['attribute_type_40']=globals()['attribute_value_40']=globals()['attribute_type_41']=globals()['attribute_value_41']=globals()['attribute_type_42']=globals()['attribute_value_42']=globals()['attribute_type_43']=globals()['attribute_value_43']=globals()['attribute_type_44']=globals()['attribute_value_44']=globals()['attribute_type_45']=globals()['attribute_value_45']=globals()['attribute_type_46']=globals()['attribute_value_46']=globals()['attribute_type_47']=globals()['attribute_value_47']=globals()['attribute_type_48']=globals()['attribute_value_48']=globals()['attribute_type_49']=globals()['attribute_value_49']=globals()['attribute_type_50']=globals()['attribute_value_50']=""
        globals()['volume_price_1']=globals()['volume_for_discount_1']=globals()['volume_discount_1']=globals()['volume_price_2']=globals()['volume_for_discount_2']=globals()['volume_discount_2']=globals()['volume_price_3']=globals()['volume_for_discount_3']=globals()['volume_discount_3']=globals()['volume_price_4']=globals()['volume_for_discount_4']=globals()['volume_discount_4']=globals()['volume_price_5']=globals()['volume_for_discount_5']=globals()['volume_discount_5']=globals()['volume_price_6']=globals()['volume_for_discount_6']=globals()['volume_discount_6']=globals()['volume_price_7']=globals()['volume_for_discount_7']=globals()['volume_discount_7']=globals()['volume_price_8']=globals()['volume_for_discount_8']=globals()['volume_discount_8']=globals()['volume_price_9']=globals()['volume_for_discount_9']=globals()['volume_discount_9']=globals()['volume_price_10']=globals()['volume_for_discount_10']=globals()['volume_discount_10']=""
        cross_referencing_product_url,cross_referencing_product_name,private_label,Stock='','','','N/A'
        data=""
        api_url1="https://www.zoro.com/product/?products={}".format((url.split("/i/")[1]).replace("/",""))
        # print("api_url=====",api_url1)
        response=get_page_response(api_url1,postmethod="get",data=data)
        # print("response====",response.text)
        json_data=json.loads(response.text)["products"][0]
        Product_Name=json_data["title"]
        if  Product_Name:
                try:  
                        Source_url=url
                        print("Source_url======",Source_url)
                        Manufacturer=json_data["brand"]
                        print("Manufacturer====",Manufacturer)
                        Item_Number=json_data["zoroNo"]
                        print("Item_Number=====",Item_Number)
                        Retail=json_data["price"]
                        print("retails=========",Retail)
                        # Minimum_Quantity=json_data["zoroMinOrderQty"]
                        Minimum_Quantity=json_data['validation']["minOrderQuantity"]
                        print("Minimum_Quantity:",Minimum_Quantity)
                        path_array=[]
                        categs=json_data["categorization"][0]
                        keylist = categs.keys()
                        keylist=sorted(keylist)
                        for x in keylist:
                                path_array.append(categs[x])
                        path= " | ".join(path_array)
                        path= "Home | {}".format(path)
                        Category= categs['categoryL1']
                        print("catagory:",Category)
                        Sub_Category= categs['categoryL2']
                        print("sub_catagory:",Sub_Category)
                        spec_list=[]
                        # print("json_data['attributes']-----",json_data["attributes"])
                        for specs in json_data["attributes"]:
                                spec_list.append("{} : {}".format(specs['name'].replace(":"," ").replace(";"," "),specs['value'].replace(":"," ").replace(";"," ")))
                        Specification= ";".join(spec_list)
                        if Specification:
                                productypeval = Specification.split(";")
                                if productypeval:
                                                        for m in range(0, len(productypeval)):
                                                                        globals()['attribute_type_%s' % str(int(m)+3)] = productypeval[m].split(':')[0]
                                                                        globals()['attribute_value_%s' % str(int(m)+3)] = productypeval[m].split(':')[1]

                                                                        # print("attribute_type_----",productypeval[m].split(':')[0])
                                                                        # print("attribute_value_----",productypeval[m].split(':')[1])

                                                                        if "Features" in productypeval[m].split(':')[0]:
                                                                                Features = productypeval[m].split(':')[1]
                                                                                print("Features------",Features)


                        # print("1")
                        
                        response=get_page_response(Source_url,postmethod="get",data="")
                        #print(response.text)
                        # print("2")
                        soup = BeautifulSoup(response.text,'html.parser')
                        Specification = soup.find("table",class_="product-specifications__table table table-striped").text.strip()
                        # print("3")
                        print("Specification-------------",Specification)

                        scrap_product_detail_response = HtmlResponse(url="my HTML string", body=response.text, encoding='utf-8')

                        try:
                                Item_Detailed=scrap_product_detail_response.xpath("//div[contains(@class,'product-description__text')]//text()").extract()[0]
                                print("item_detailed======",Item_Detailed)
                        except:
                                Item_Detailed = ""  
                        # if Item_Detailed:
                        #                 Item_Detailed= ' '.join(x.strip() for x in Item_Detailed)
                        #                 Item_Detailed=Item_Detailed.strip()
                        #                 Item_Detailed=re.sub("\s\s+" , " ", Item_Detailed)
                        # print("item_detailed======",Item_Detailed)
                        Manufacturer_Number=scrap_product_detail_response.xpath("//li[contains(@class,'product-identifiers__mfr-no')]//span//text()").extract_first()
                        if Manufacturer_Number: Manufacturer_Number = Manufacturer_Number.strip()
                        print("manufacturer_no:",Manufacturer_Number)
                        Package_Size=scrap_product_detail_response.xpath("//span[contains(@class,'product-price__unit-of-measure')]//text()").extract_first()
                        if Package_Size: Package_Size = (Package_Size.strip()).replace("/","")

                        # print(soup)
                        try:
                                Order_Unit = soup.find("div",class_="product-overview product-details-page__overview").find("div",class_="product-price").text.split(" of ")[1].strip()
                                print("order_unit-------",Order_Unit)
                        except:
                                # print("eeeee---",e)
                            Order_Unit = " "
                        # Shipping_Information=scrap_product_detail_response.xpath("//a[@data-za='header-shipping']/text()").extract()[0].strip()
                        # print("Shipping_Information:",Shipping_Information)
                        # if Shipping_Information:
                        #                 Shipping_Information= ' '.join(x.strip() for x in Shipping_Information)
                        #                 Shipping_Information=Shipping_Information.strip()
                        #                 Shipping_Information=re.sub("\s\s+" , " ", Shipping_Information)

                        Stock= json_data["validation"]["nsNo"]
                        if Stock != 0:
                                Stock="Yes"
                        else:
                                Stock="No"

                        Country_of_Origin=scrap_product_detail_response.xpath("//td//strong[contains(text(),'Country of')]//following-sibling::text()").extract_first()
                        if Country_of_Origin: Country_of_Origin = (Country_of_Origin.strip()).replace(":","")
                        try:
                                globals()['attribute_type_%s' % str(int(m+1)+3)] = "Country of Origin"
                                globals()['attribute_value_%s' % str(int(m+1)+3)] = Country_of_Origin
                                # print("attribute_type_----",productypeval[m].split(':')[0])
                                # print("attribute_value_----",productypeval[m].split(':')[1])
                        except:
                                m = 0
                                globals()['attribute_type_%s' % str(int(m)+3)] = "Country of Origin"
                                globals()['attribute_value_%s' % str(int(m)+3)] = Country_of_Origin
                                # print("attribute_type_----",globals()['attribute_type_%s' % str(int(m+1)+1)])
                                # print("attribute_value_----",globals()['attribute_value_%s' % str(int(m+1)+1)])
                        globals()['attribute_type_1'] = "Zoro:"
                        globals()['attribute_value_1'] = Item_Number
                        globals()['attribute_type_2'] = "Mfr:"
                        globals()['attribute_value_2'] = Manufacturer_Number

                        # print("attribute_type_"str(int(m+1)+1"======",
                        # print("attribute_type_----",productypeval[m].split(':')[1])
                        
                        c_code="USD"

                        UPC=scrap_product_detail_response.xpath("//td//strong[contains(text(),'UPC')]//following-sibling::text()").extract_first()
                        if UPC: UPC = (UPC.strip()).replace(":","")

                        try:
                                caution=scrap_product_detail_response.xpath("//td[@data-za='product-compliance-text-restricted-states']/text()").extract()[0].strip()
                                print("Caution:",caution)
                        # if caution:
                        #                 caution= ' '.join(x.strip() for x in caution)
                        #                 caution=caution.strip()
                        #                 caution=re.sub("\s\s+" , " ", caution)
                        # Features= scrap_product_detail_response.xpath("//ul[@class='product-details__list']/li//text()").extract()
                        # print("features:",Features)
                        except:
                                caution = " "

                        # if Features:
                        #                 Features= ' '.join(x.strip() for x in Features)
                        #                 Features=Features.strip()
                        #                 Features=re.sub("\s\s+" , " ", Features)
                        # print("Features------",Features)
                        # Attrs = scrap_product_detail_response.xpath("//ul[@class='product-details__list']/li//text()").extract()

                        
                        column=[Manufacturer,Manufacturer,Manufacturer_Number,Item_Number,UPC,' ',Product_Name,Item_Detailed,Package_Size,Order_Unit,Minimum_Quantity,c_code,without_tax,vat,str(MSRP_Price),
                                str(Retail),str(0),str(Discount),volume_price_1,volume_for_discount_1,volume_discount_1,volume_price_2,volume_for_discount_2,volume_discount_2,volume_price_3,volume_for_discount_3,volume_discount_3,volume_price_4,volume_for_discount_4,volume_discount_4,volume_price_5,volume_for_discount_5,volume_discount_5,volume_price_6,volume_for_discount_6,volume_discount_6,volume_price_7,volume_for_discount_7,volume_discount_7,volume_price_8,volume_for_discount_8,volume_discount_8,volume_price_9,volume_for_discount_9,volume_discount_9,volume_price_10,volume_for_discount_10,volume_discount_10,attributes_Technical_Specs,
                                Features,Specification,Application,caution,Stock,Category,Sub_Category,Country_of_Origin,Catelog,Guarantee_Information,Shipping_Information,path,Source_url,cross_referencing_product_url,cross_referencing_product_name,private_label,attribute_type_1,attribute_value_1,attribute_type_2,attribute_value_2,attribute_type_3,attribute_value_3,attribute_type_4,attribute_value_4,attribute_type_5,attribute_value_5,attribute_type_6,attribute_value_6,attribute_type_7,attribute_value_7,attribute_type_8,attribute_value_8,attribute_type_9,attribute_value_9,attribute_type_10,attribute_value_10,attribute_type_11,attribute_value_11,attribute_type_12,attribute_value_12,attribute_type_13,attribute_value_13,attribute_type_14,attribute_value_14,attribute_type_15,attribute_value_15,attribute_type_16,attribute_value_16,attribute_type_17,attribute_value_17,attribute_type_18,attribute_value_18,attribute_type_19,attribute_value_19,attribute_type_20,attribute_value_20,attribute_type_21,attribute_value_21,attribute_type_22,attribute_value_22,attribute_type_23,attribute_value_23,attribute_type_24,attribute_value_24,attribute_type_25,attribute_value_25,attribute_type_26,attribute_value_26,attribute_type_27,attribute_value_27,attribute_type_28,attribute_value_28,attribute_type_29,attribute_value_29,attribute_type_30,attribute_value_30,attribute_type_31,attribute_value_31,attribute_type_32,attribute_value_32,attribute_type_33,attribute_value_33,attribute_type_34,attribute_value_34,attribute_type_35,attribute_value_35,attribute_type_36,attribute_value_36,attribute_type_37,attribute_value_37,attribute_type_38,attribute_value_38,attribute_type_39,attribute_value_39,attribute_type_40,attribute_value_40,attribute_type_41,attribute_value_41,attribute_type_42,attribute_value_42,attribute_type_43,attribute_value_43,attribute_type_44,attribute_value_44,attribute_type_45,attribute_value_45,attribute_type_46,attribute_value_46,attribute_type_47,attribute_value_47,attribute_type_48,attribute_value_48,attribute_type_49,attribute_value_49,attribute_type_50,attribute_value_50]
                        
                        
                        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname,user,host,password))
                        cur = conn.cursor(cursor_factory=DictCursor)   
                        cur.execute("select id from {} where item_number='{}'".format(TABLE_NAME,Item_Number))
                        res = cur.fetchall()
                        conn.commit()
                        conn.rollback()
                        conn.close()
                        #print(f"No. of Occurence {print(len(res))}")
                        # print("RES----",res)
                        if  len(res)== 0:
                                z = str("%"+"s")
                                for i in range(1,len(column)):
                                        z += str(","+"%"+"s")
                                try:
                                        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname,user,host,password))
                                        # conn = psycopg2.connect("dbname='Ind_test' user='postgres' host='167.xxx.xxx.xxx' password='xxx@123'")
                                        cur = conn.cursor(cursor_factory=DictCursor)
                                        cur.execute("insert into "+TABLE_NAME+" values (DEFAULT,"+z+")", column)
                                        print("success")
                                        conn.commit()
                                        # conn2 = psycopg2.connect("dbname='industryparts' user='postgres' host='xxxxx' password='xxxxx@2018'")
                                        # cur2 = conn2.cursor()
                                        cur.execute("update "+TABLE_NAME+"_product_urls set scraped=%s where product_url=%s",(1,url))
                                        conn.commit()
                                        # update_command=f"update {TABLE_NAME}_product_urls set scraped={1} where product_url='{url}'"
                                        # update_command="update "+TABLE_NAME+"_product_urls set scraped=True where product_url='{url}'"
                                        # print(update_command)
                                        print("URL updated as 1")
                                        # cur2.execute(update_command)
                                        # conn2.commit()
                                        # print("here it is alll========>")
                                except IntegrityError:
                                        conn.rollback()
                                except Exception as e:
                                        print(e)
                                        conn.rollback()    
                                conn.close()
                                # conn2.close()
                                del column
                        else:
                                print("Duplicate Item found")
                                        
                except Exception as ex:
                        print("Exception {}; => Base Url: {}".format(ex, url))


def main():
        print("Main function")
        conn = psycopg2.connect("dbname='industryparts' user='postgres' host='159.65.xxx.xxx' password='xxx@2018'")
        #   conn = psycopg2.connect("dbname='Ind_test' user='postgres' host='167.99.xx.xxx' password='xxxx@123'")
        cur = conn.cursor()
        #select product_url from {}_product_urls where scraped=false and id between 0 and 1000000 order by id asc;
        #   cur.execute("select product_url from {}_product_urls where scraped={}  order by id asc;".format(TABLE_NAME,"0"))
        cur.execute("select distinct product_url from " + TABLE_NAME + "_product_urls vpu left join " + TABLE_NAME + " v on vpu.product_url = v.source_url where v.source_url is NULL")
        res = cur.fetchall() 
        print(("Total product Count :", len(res)))
        sub_list_len=str(len(res)/int(core_count)+7).split(".")[0]
        pool_lists=[res[i:i+int(core_count)+7] for i in range(0, len(res), int(core_count)+7)]
        #   print("RES----",res)
        del res
        # for urlList in pool_lists:
                # print("no of data===",len(pool_lists))
                # print("urlList-----",urlList)
        p = Pool(int(core_count)+7) 
#p = Pool(1)
        p.map(get_data, pool_lists)
        p.terminate()
        p.join()
        p.close()


if __name__ == "__main__":
        main()
  

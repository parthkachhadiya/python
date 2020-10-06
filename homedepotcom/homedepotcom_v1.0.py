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
import os
# from get_proxy import myproxy
# from save_xlsx import save_sheet
#from fake_useragent import UserAgent
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import IntegrityError
from multiprocessing import Process, Pool
import random
import json

ua = UserAgent()
TABLE_NAME = "homedepot"
core_count=os.cpu_count()
print("Total CPU Core Available: {}".format(core_count))
print("No. of workers: {}".format(int(core_count)+7))

conn = psycopg2.connect("dbname='industryparts' user='postgres' host='159.65.xxx.xx' password='xxx@2018'")
cur = conn.cursor(cursor_factory=DictCursor)

def get_data(url):
      #url="https://www.homedepot.com/p/MODWAY-Prospect-Channel-Tufted-Gray-Upholstered-Velvet-Loveseat-EEI-3137-GRY/309742165"
    #   proxies = {'http': 'http://lum-customer-wmtp-zone-xxxx:xxxx@zproxy.lum-xxx.io:22225',
    #             'https': 'http://lum-customer-wmtp-zone-xxx:np98itf6sdic@zproxy.lum-xxxx.io:22225'
    #             }
     
      print(url)
    
      manufacturer,manufacturer_number,item_number,UPC,unspsc,product_name,item_detailed,Package_Size,minimum_quantity,currency_code,without_tax,vat,msrp_list_price,retail_price_your_price,get_this_price,discount_you_save_amount,discount_you_save_percentage,volume_price_1,volume_for_discount_1,volume_discount_1,volume_price_2,volume_for_discount_2,volume_discount_2,volume_price_3,volume_for_discount_3,volume_discount_3,volume_price_4,volume_for_discount_4,volume_discount_4,volume_price_5,volume_for_discount_5,volume_discount_5,volume_price_6,volume_for_discount_6,volume_discount_6,volume_price_7,volume_for_discount_7,volume_discount_7,volume_price_8,volume_for_discount_8,volume_discount_8,volume_price_9,volume_for_discount_9,volume_discount_9,volume_price_10,volume_for_discount_10,volume_discount_10,product_attributes_technical_specs,features,specification,applications,caution,in_stock,category,sub_category,country_of_origin,catalog,guarantee_information,shipping_information,path,source_url,attribute_type_1,attribute_value_1,attribute_type_2,attribute_value_2,attribute_type_3,attribute_value_3,attribute_type_4,attribute_value_4,attribute_type_5,attribute_value_5,attribute_type_6,attribute_value_6,attribute_type_7,attribute_value_7,attribute_type_8,attribute_value_8,attribute_type_9,attribute_value_9,attribute_type_10,attribute_value_10,attribute_type_11,attribute_value_11,attribute_type_12,attribute_value_12,attribute_type_13,attribute_value_13,attribute_type_14,attribute_value_14,attribute_type_15,attribute_value_15,attribute_type_16,attribute_value_16,attribute_type_17,attribute_value_17,attribute_type_18,attribute_value_18,attribute_type_19,attribute_value_19,attribute_type_20,attribute_value_20,attribute_type_21,attribute_value_21,attribute_type_22,attribute_value_22,attribute_type_23,attribute_value_23,attribute_type_24,attribute_value_24,attribute_type_25,attribute_value_25,attribute_type_26,attribute_value_26,attribute_type_27,attribute_value_27,attribute_type_28,attribute_value_28,attribute_type_29,attribute_value_29,attribute_type_30,attribute_value_30,attribute_type_31,attribute_value_31,attribute_type_32,attribute_value_32,attribute_type_33,attribute_value_33,attribute_type_34,attribute_value_34,attribute_type_35,attribute_value_35,attribute_type_36,attribute_value_36,attribute_type_37,attribute_value_37,attribute_type_38,attribute_value_38,attribute_type_39,attribute_value_39,attribute_type_40,attribute_value_40,attribute_type_41,attribute_value_41,attribute_type_42,attribute_value_42,attribute_type_43,attribute_value_43,attribute_type_44,attribute_value_44,attribute_type_45,attribute_value_45,attribute_type_46,attribute_value_46,attribute_type_47,attribute_value_47,attribute_type_48,attribute_value_48,attribute_type_49,attribute_value_49,attribute_type_50,attribute_value_50="","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""
      Source_Website,Manufacturer,Manufacturer_Number,Item_Number,UNSPSC,Product_Name,Product_details,Quantity,Specification,Application,Category,Country_of_Origin,Catelog='','','','','','','','','','','','',''
      Source_Website,Manufacturer,Manufacturer_Number,Item_Number,UNSPSC,Product_Name,Item_Detailed,MSRP_Price,Product_Attributes_Technical_Specs,Stock,Category,Sub_Category,Shipping_Information,path,Source_url,Currency_Code="","","","","","","","","","","","","","","",""
      Features,Source_Website,Manufacturer,Item_Number,Product_Name,Item_Detailed,Package_Size,Minimum_Quantity,MSRP_Price,Retail_Price,Stock,Category,Sub_Category,Catalog,Shipping_Information,path,Source_url,C_code="","","","","","","","","","","","","","","","","",""
      cross_referencing_product_url,cross_referencing_product_name,private_label='','','' 
      Brand,Order_Unit='',''
      cross_referencing_product_url=''
      cross_referencing_product_name=''
      private_label='No'
      ch = 0 
      while ch<6:  
        try:
            ua = UserAgent()
            proxies = {'http': 'http://xxx:@proxy.xxx.com:8010/',
                    "https":"http://xxx:@proxy.xxx.com:8010/"} 
            
            headers={
            "user-agent":ua.random, 
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"en-US,en;q=0.5",
            "Host":"www.homedepot.com", 
            "Upgrade-Insecure-Requests":"1", 
            "Connection":"keep-alive",
            "Cache-Control":"max-age=0", 
            } 
            response=requests.get(url,headers=headers,proxies=proxy,verify='xxxx-ca.crt')
            print(response) 
            status=response.status_code
        except:
            status=300
        if status ==403 or status ==404:
            ch +=1
            if ch ==6:
                return  
        elif status !=200: 
            #ua = UserAgent()
            proxies=proxies
            print("Retrying..")
        else:
            break
      if 'The product you are trying to view is not currently available.' in response.text:
          return
      try:    
        soup = BeautifulSoup(response.text, "html.parser")
        Source_url=url
        
        try:
            Manufacturer=soup.find('div',{'class':'sticky_brand_info'}).text.strip()
        except:
            Manufacturer="" 
            try:
                Manufacturer=soup.find('span',{'class':'brand'}).text.strip()
            except:
                pass
                print("Error: Manufacturer")
        #print("manuf-------------------",Manufacturer)
        try:
            Manufacturer_Number=soup.find('div',{'class':'sticky_model_info'}).text.split('#')[-1].strip() 
            if len(Manufacturer_Number) == 0: 
                Manufacturer_Number = soup.find('div',{'class':'sticky_model_info'}).text.split('#')[-2].strip() 
            #print("*******************",Manufacturer_Number)
        except:
             
            Manufacturer_Number=""
            try:
                Manufacturer_Number=soup.find('span',{'class':'product-infobar__detail'}).text.split('#')[-1].strip()
            except:
                try:
                    MFs =soup.findAll("script")
                    print("needeeeed")
                    for MF in MFs: 
                        if "window['__BOOTSTRAPPED_PROPS__']" in MF.text: 
                            #print(MF.text)
                            break
                    Manufacturer_Numbers = MF.text.split("['SkuService'] = ")[1]  
                    Manufacturer_Number = json.loads(Manufacturer_Numbers)['sku']['info']['modelNumber']
                    try:
                        if len(Manufacturer) == 0:
                            Manufacturer =  json.loads(Manufacturer_Numbers)['sku']['info']['brandName']  
                    except:
                        pass 
                    #print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")           
                except Exception as e:  
                    #print("erroooooooorrrrrr",e)        
                    print("Error: Manufacturer_Number")
        print("manuf-------------------",Manufacturer_Number)
        try:
            Item_Number=soup.find('span',{'id':'product_internet_number'}).text 
        except:
            try:
                Item_Number=soup.findAll('span',{'class':'product-infobar__detail'})[1].text.split('#')[-1].strip()
            except:
                try:
                    Item_Number = url.split('/')[-1] 
                except:  
                    Item_Number=""
                #print("Item_Number") 
        #print(Item_Number)
        try:
            Product_Name=soup.find('h1').text.strip()
        except Exception as e:
            print("Error in pro name:",e)
            Product_Name=""
        #print(Product_Name)
        try:
            try: 
                Item_Detailed=soup.find('div',{'class':'card__summary with-fade'})
                try:
                    Item_Detailed.find("script").extract()
                except:
                    pass
                Item_Detailed=Item_Detailed.text.strip()
            except Exception as e:
                Item_Detailed=""
                try:
                    Item_Detailed=soup.find('div',{'class':'grid product-description__main-description'}).text
                except: 
                    pass

        except:
            try:
                Item_Detailed=soup.find('div',{'class':'main_description col-12 col-md-12'}).text.strip()
            except:
                Item_Detailed=""
                print("Error: Item_Detailed")
        #print(Item_Detailed)
        try:
            cas=soup.findAll('script',{'type':"text/javascript"})
            for ca in cas: 
                if 'bcHtml' in ca.text:
                    ct=ca.text[30:-6]
            cj=json.loads(ct)
            sp=BeautifulSoup(cj['bcHtml'], "html.parser")
            pathh=[spe.text for spe in sp.findAll('a')] 
            path=""
            Category=pathh[0]
            try:
                Sub_Category=pathh[1] 
            except:
                Sub_Category=""
            path='Home / '+' / '.join(pathh) 

        except Exception as e:
            path,Category,Sub_Category="","",""
            cas=soup.find('ul',{'class':'breadcrumb__header'}).findAll('a')
            pathh=[i.text for i in cas]
            Category=pathh[1]
            try:
                Sub_Category=pathh[2]
            except:
                Sub_Category=""
            path=' / '.join(pathh)
        #print(Sub_Category,Category,path)
        try:
            Package_Size=soup.find('span',{'class':'price__uom'}).text.split('/')[-1]
        except Exception as e:
            Package_Size="" 
            print("Error: Package_Size")
        #print(Package_Size)
        Retail=""
        Minimum_Quantity=""
        Discount=""
        DisP="" 
        try:
            Stock = soup.find('span',{'class':'u__text--danger'}).get_text()
            if "Discontinued" in Stock:
                Stock='discontinued'
            if Stock == '' :
                Stock = "N/A"
        except Exception as e:
            print("Errr in stock",e)
        print('here it is')
        #   try:
        #     Retail = soup.find('span',{'id':'ajaxPriceAlt'}).get_text()
        #   except:
        #     try:
        #       Retail = soup.find('input',{'id':'ciItemPrice'})['value']
        #     except:
        #       Retail = ""
        #   print("yours_retail--------",Retail)   
        #   try:
        #     MSRP_Price = soup.find('span',{'id':'ajaxPriceStrikeThru'}).get_text()
        #   except:
        #     MSRP_Price = ""   
        #   print("yours_MSRP_Price--------",MSRP_Price)   
        try:
            print("try 1")
            Retail = soup.find('span',{'id':'ajaxPriceAlt'}).get_text()
            Retail = Retail.replace("$",'').strip()
        except:
            try:
                print("try 2")
                Retail = soup.find('input',{'id':'ciItemPrice'})['value']
                Retail = Retail.replace("$",'').strip()
            except:
                try:
                    Rets =soup.findAll("script")
                    for MF in Rets:
                        if "window['__BOOTSTRAPPED_PROPS__']" in MF.text:
                            #print(MF.text)
                            break 
                    RP = MF.text.split("['SkuService'] = ")[1]  
                    # print(RP)
                    Retail =  json.loads(RP)['sku']['storeSkus'][0]['pricing']['originalPrice']
                    print("reatials price ====>>>>")
                    print(Retail)
                    print("try 3")
                     

                except:
                    try:
                        Ret = soup.find('div',{'class':'price-format__large price-format__main-price'}).findAll('span')
                    
                        Retail = Ret[1].get_text() +"."+Ret[2].get_text()    
                        print("try 4")
                        # Rets =soup.findAll("script")
                        # for MF in Rets: 
                        #     if "window['__BOOTSTRAPPED_PROPS__']" in MF.text:
                        #         #print(MF.text)
                        #         break
                        # RP = MF.text.split("['SkuService'] = ")[1]  
                        # print(RP)
                        # Retail =  json.loads(RP)['sku']['storeSkus'][0]['pricing']['originalPrice']
                        # print("reatials price ====>>>>")
                        # print(Retail)
                    except:         
                        Retail = ""
        print("yours_retail--------",Retail)   
        try:
            MSRP_Price = soup.find('span',{'class':'pStrikeThru'}).get_text()
            MSRP_Price = MSRP_Price.replace("$",'').strip()
        except:
            MSRP_Price = ""   
        print("yours_MSRP_Price--------",MSRP_Price) 
        try: 
            Discount = float(MSRP_Price)-float(Retail)
            Discount = round(Discount,2)
            #print('Discount',Discount)
            DisP = (Discount/float(MSRP_Price))*100
            DisP = round(DisP,2)
            print(Discount)
            print(DisP)
        except Exception as e:
            print(e) 

        try:
            Package_Size = soup.find('div',class_='buybox_case_pricing_covers').get_text()
            Package_Size = Package_Size.strip()
        except:
            Package_Size = ""  
        print("Package_Size----------",Package_Size)    

        #print(MSRP_Price,Retail,Minimum_Quantity,Discount,DisP)
 

        try:
            atts=[]
            extra_ats=soup.findAll('h2',{'class':'product_details'})
            if len(extra_ats)>2:
                for ea in extra_ats[2:]:
                    atts.append(ea.text.split('#')[0].strip())
                    atts.append(ea.text.split('#')[1].strip())
            Guarantee_Information=""
            Product_Attributes_Technical_Specs=""
            pat=soup.find('div',{'id':'specsContainer'})
            label=pat.findAll('div',{'class':'col-6 specs__cell specs__cell--label'})
            label1=pat.findAll('div',{'class':"specs__cell col__6-12"})
            if len(label)!=len(label1):
                label1=pat.findAll('div',{'class':"col-6 specs__cell"})
            for l,l1 in zip(label,label1):
                if l.text=='Manufacturer Warranty' or l.text=='Warranty Information':
                    Guarantee_Information=l1.text
                elif l.text=='Package Quantity':
            
                    Package_Size=l1.text
                else: 
                    Product_Attributes_Technical_Specs+=l.text+" : "+l1.text+","+"\n"
                    atts.append(l.text)
                    atts.append(l1.text)
        except:
            Product_Attributes_Technical_Specs=""
            atts=[]
            Guarantee_Information=""
            try:
                pat=soup.find('div',{'class':'desktop-items'})
                # print(pat)
                label=pat.findAll('div',{'class':'specs__cell specs__cell__label col__6-12'})
                label1=pat.findAll('div',{'class':'specs__cell col__6-12'})
                # print("here======================") 
                for l,l1 in zip(label,label1):
                    # print("l.text===>>>",l.text)
                    # print("l1.text===>>>",l1.text)
                    if l.text=='Manufacturer Warranty' or l.text=='Warranty Information':
                        Guarantee_Information=l1.text
                    elif l.text=='Package Quantity':
                
                        Package_Size=l1.text
                    else:
                        Product_Attributes_Technical_Specs+=l.text+" : "+l1.text+","+"\n"
                        atts.append(l.text)
                        atts.append(l1.text)
            except Exception as e: 
                print("Error: Product_Attributes_Technical_Specs",e)
            try:
                print("try")
                pat=soup.find('div',{'id':'specifications'})
                # print(pat)
                label=pat.findAll('div',{'class':'specs__cell specs__cell__label col__6-12'})
                label1=pat.findAll('div',{'class':'specs__cell col__6-12'})
                print("here======================")
                for l,l1 in zip(label,label1):
                    # print("l.text===>>>",l.text)
                    # print("l1.text===>>>",l1.text)
                    if l.text=='Manufacturer Warranty' or l.text=='Warranty Information':
                        Guarantee_Information=l1.text
                    elif l.text=='Package Quantity':
                
                        Package_Size=l1.text
                    else: 
                        Product_Attributes_Technical_Specs+=l.text+" : "+l1.text+","+"\n"
                        atts.append(l.text)
                        atts.append(l1.text)
            except Exception as e:
                print("Error: Product_Attributes_Technical_Specs",e)


        api_url = "https://www.homedepot.com/p/svcs/frontEndModel/"+Item_Number
        api_headers = {
        'accept': "*/*",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.9,hi;q=0.8",
        'cookie': "s_ecid=MCMID%7C05920873427145791123411558718051684276",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        }

        c_code="USD"
        try:
            discheq=soup.find('span',{'class':'u__text--danger'}).text
            discheq=False
        except: 
            discheq=True
        Minimum_Quantity = ""
        try:
            Minimum_ = soup.find("script",id = "item_pod").text
            ssp = BeautifulSoup(Minimum_,'lxml')
            Minimum_Quantity = ssp.find("div",class_='multiAtc-button-wrapper').find('a')['data-quantity']
        except:
            pass  
        print('Minimum_Quantity------------------->sssss',Minimum_Quantity)
        try:
            Package_Size = Package_Size.replace("/",'')
        except:
            pass   
        try:
            Brand_data_fbr=[]
            url_data_fbr=[]
            name_data_fbr=[]
            div_fbr_trs = soup.find("div",id = "fbr-container").find('div',{'class':'fbr-wrapper'}).find('table',{'class':'main-table'}).findAll('tr')
            kk=0
            for div_fbr_tr in div_fbr_trs:
                if 'class="ratings"' not in str(div_fbr_tr) or 'class="pricing"' not in str(div_fbr_tr):
                    flag=''
                    tt=0
                    for td in div_fbr_tr.findAll('td'):
                        # print(td.get_text()) 
                        if tt==1:
                            if "Name" in flag:
                                name_data_fbr.append(td.get_text().strip())
                            if "Brand" in flag:
                                Brand_data_fbr.append(td.get_text().strip())
                            try:
                                if flag=='':
                                    url_data_fbr.append('https://www.homedepot.com'+td.find('a')['href'])   
                            except:
                                pass
                        if tt==0:
                            tt=1
                            flag=td.get_text()
            if len(name_data_fbr)==len(Brand_data_fbr):
                for idx, val in enumerate(name_data_fbr):
                    if "The Home Depot" in  Brand_data_fbr[idx]:
                        cross_referencing_product_url=url_data_fbr[idx]
                        cross_referencing_product_name=val
                        private_label='Yes'
                        if cross_referencing_product_url!=source_url:
                            break

            # print("this is data of fr========================")
            # print("cross_referencing_product_url",cross_referencing_product_url)
            # print('cross_referencing_product_name',cross_referencing_product_name)
            print('private_label=================>>',private_label)
        except Exception as e:
            print("cross refrence Err:",e)
        try:
            print(atts)
            my_atts = soup.findAll('div',class_='specifications__row col__12-12 col__12-12--xs col__12-12--sm col__6-12--md')
            if len(my_atts)!=0:
                if len(atts) !=len(my_atts):
                        atts=[]
                        try:
                            print("here ")
                            Product_Attributes_Technical_Specs=""
                            my_atts = soup.findAll('div',class_='specifications__row col__12-12 col__12-12--xs col__12-12--sm col__6-12--md')
                            for my_at in my_atts:
                                req_att = my_at.findAll('div')
                                req_at1 = req_att[0].get_text()
                                req_val1 = req_att[1].get_text()
                                if len(req_at1) != 0:
                                    atts.append(req_at1.strip())
                                    atts.append(req_val1.strip())
                                if 'Warranty' in  req_at1:
                                    Guarantee_Information =  req_val1
                                if 'Package Quantity' in  req_at1:
                                    Package_Size = req_val1 
                                # my_atts=list(dict.fromkeys(my_atts))
                                Product_Attributes_Technical_Specs +=   req_at1 +" : "+  req_val1 + ","+"\n"     
                        except Exception as e:
                            print("err in attr",e)
                            pass     
        except:
            pass
        print("product Product_Attributes_Technical_Specs===>>>>",Product_Attributes_Technical_Specs)
        #column=[Source_Website,Manufacturer,Manufacturer_Number,Item_Number,'','',Product_Name,Item_Detailed,Package_Size,Minimum_Quantity,MSRP_Price,Retail,'0',Discount,DisP,Product_Attributes_Technical_Specs,'','','','','',Category,Sub_Category,'','',Guarantee_Information,'',path,Source_url,c_code]
        #api_response = requests.request("GET", api_url,headers=api_headers)
        column=['homedepot.com',Manufacturer,Brand,Manufacturer_Number,Item_Number,'','',Product_Name,Item_Detailed,Package_Size,Order_Unit,Minimum_Quantity,c_code,without_tax,vat,str(MSRP_Price),
            str(Retail),str(Discount),DisP,volume_price_1,volume_for_discount_1,volume_discount_1,volume_price_2,volume_for_discount_2,volume_discount_2,volume_price_3,volume_for_discount_3,volume_discount_3,volume_price_4,volume_for_discount_4,volume_discount_4,volume_price_5,volume_for_discount_5,volume_discount_5,volume_price_6,volume_for_discount_6,volume_discount_6,volume_price_7,volume_for_discount_7,volume_discount_7,volume_price_8,volume_for_discount_8,volume_discount_8,volume_price_9,volume_for_discount_9,volume_discount_9,volume_price_10,volume_for_discount_10,volume_discount_10,Product_Attributes_Technical_Specs,
            Features,Specification,Application,caution,Stock,Category,Sub_Category,Country_of_Origin,Catelog,Guarantee_Information,Shipping_Information,path,Source_url,cross_referencing_product_url,cross_referencing_product_name,private_label]

        column.extend(atts)
        print(len(column))
        print(column)
        z = str("%"+"s")
        for i in range(1,len(column)):
            z += str(","+"%"+"s")
        try:
            conn = psycopg2.connect("dbname='industryparts' user='postgres' host='159.65.xxxx.xxx' password='xxxx@2018'")
            cur = conn.cursor(cursor_factory=DictCursor)
            cur.execute("insert into homedepot values (DEFAULT,"+z+")", column)
            conn.commit() 
            cur.execute("update homedepot_product_urls set scraped=%s where product_url=%s",(True,Source_url))
            conn.commit()
            print("Saved===")
        except IntegrityError:
            conn.rollback()
        except Exception as e:
            print(e)
            conn.rollback()    
        conn.close()
        del column    
      except:
          pass


def main(from_c,to_c): 
    
    # get_data('https://www.homedepot.com/p/Caroline-s-Treasures-14-in-x-21-in-Multicolor-Fish-Trout-Dish-Drying-Mat-8770DDM/306100862')
    # -----------------------------------------------------------------------
    cur.execute("select product_url from homedepot_product_urls where scraped=false")
    res = cur.fetchall()
    print(("Total product Count :", len(res)))
    top_index = (to_c-1)*int((len(res)/from_c))
    end_index = top_index + int((len(res)/from_c))
    print((len(res), top_index, end_index))
    total_result = len(res[top_index:end_index])
    urlList = [row[0] for row in res[top_index:end_index]]
    del res

    p = Pool(int(sys.argv[3]))
    p.map(get_data, urlList)
    # --------------------------------------------------------------


    # print(("Total product Count :", len(res)))
    # sub_list_len=str(len(res)/int(core_count)+7).split(".")[0]
    # pool_lists=[res[i:i+int(core_count)+7] for i in range(0, len(res), int(core_count)+7)]
    # del res
    # for urlList in pool_lists:
    #     print(urlList)
    #     p = Pool(int(core_count)+7) 
    #     #p = Pool(1)
    #     p.map(get_data, urlList) 
    #     p.terminate()
    #     p.join()
    #     p.close()

if __name__ == "__main__":
  main(int(sys.argv[1]), int(sys.argv[2]))

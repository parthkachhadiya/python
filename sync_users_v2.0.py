# from shopifyapi import ShopifyConnection
from jsondiff import diff
import pprint
import json
import time
import pandas
# from sync import AllSync
import pickle
from operator import itemgetter
from datetime import datetime
import datetime
import logging
from multiprocessing import Pool, Value
# import shopify_conn_info as conninfo
import shopify
import pyodbc
import requests
import sys
import pandas as pd
import csv
from os.path import isfile, join
from os import listdir
import urllib
from pytz import timezone
import threading
from multiprocessing import Process, Pool
import multiprocessing
from functools import partial
from contextlib import contextmanager
from datetime import datetime,timedelta
headers = {"Accept": "application/json", "Content-Type": "application/json"}
API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
PASSWORD = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
shop_url_1 = "https://%s:%s@mirrormatellc.myshopify.com/admin" % (API_KEY, PASSWORD)
shopify.ShopifyResource.set_site(shop_url_1)

def sync_updatenotes(cust_id):
    print("cust_id",cust_id)
    try:
        print(shop_url_1+"/customers/"+str(cust_id)+"/metafields.json")
        data1 = requests.get(shop_url_1+"/customers/"+str(cust_id)+"/metafields.json",headers=headers) 
        json_metfield=data1.json()
        flag=0
        for metafields_data in json_metfield['metafields']:
            if "ARDivisionNo" in metafields_data['key']:
                ardivision_number=str(metafields_data['value'])
                try:
                    if "20" in ardivision_number[:2] or "30" in ardivision_number[:2] or "22" in ardivision_number[:2] or "23" in ardivision_number[:2] or "31" in ardivision_number[:2]:
                        flag=1
                except:
                    flag=0
        if flag==1:
            if len(json_metfield['metafields'])>47:
                billing=''
                ch=True
                while ch:
                    try:
                        customer_json = requests.get(shop_url_1+"/customers/"+str(cust_id)+".json",headers=headers).json()
                        print(customer_json['customer']['id'])
                        c_email=customer_json['customer']['email']
                        c_id=customer_json['customer']['id']
                        break
                    except:
                        pass
                # customer_json
                pricelevel=taxschedule=customer_acc=billing_address1=billing_address2=billing_city=billing_state=billing_zip=billing_country=''
                for metafields_data in json_metfield['metafields']:
                    if "CustomerNo" in metafields_data['key']:
                        customer_acc=metafields_data['value']
                        # string_customer_note+="Customer Account # : "+str(metafields_data['value'])+" \n"
                    if "company_name" in metafields_data['key']:
                        company_name=str(metafields_data['value'])
                    if "billing_address1" in metafields_data['key']:
                        if str(metafields_data['value'])!="-":
                            billing_address1=str(metafields_data['value'])+" ,"
                    if "billing_address2" in metafields_data['key']:
                        if str(metafields_data['value'])!="-":
                            billing_address2=str(metafields_data['value'])+" ,"
                    if "billing_city" in metafields_data['key']:
                        if str(metafields_data['value'])!="-":
                            billing_city=str(metafields_data['value'])+" ,"
                    if "billing_state" in metafields_data['key']:
                        if str(metafields_data['value'])!="-":
                            billing_state=str(metafields_data['value'])+" ,"
                    if "billing_zip" in metafields_data['key']:
                        if str(metafields_data['value'])!="-":
                            billing_zip=str(metafields_data['value'])+" ,"
                    if "billing_country" in metafields_data['key']:
                        if str(metafields_data['value'])!="-":
                            billing_country=str(metafields_data['value'])
                    if "billing_phone" in metafields_data['key']:
                        billing_phone=str(metafields_data['value'])
                    if "TermsCode" in metafields_data['key']:
                        termscode=str(metafields_data['value'])
                    if  metafields_data['key']=="PriceLevel":
                        pricelevel=str(metafields_data['value'])
                    if "TaxSchedule" in metafields_data['key']:
                        taxschedule=str(metafields_data['value'])
                bill_address=billing_address1+billing_address2+billing_city+billing_state+billing_zip+billing_country
                billing_info='Sage Billing Info \nCustomer Account #: '+str(customer_acc)+'\nCustomer Name: ' +str(company_name)+'\nCustomer Address:' +bill_address+'\nSales Person: - \nCustomer Email: ' +c_email+' \nCustomer Phone :' +billing_phone+' \nTermsCode: '+str(termscode)+'\nPrimary Contact: -\nTAX Schedule: '+str(taxschedule)+'\nPrice Level: '+pricelevel+' \n'
                print("there cms is billing info \n",billing_info)
                try:
                    c = shopify.Customer.find(c_id)
                    c.note = billing_info
                    c.save()
                    print("-------update new notes--------- ")
                except:
                    pass
    except Exception as e:
        print("error :",e)

def get_users_data_2():
    try:
        resources = []
        page=0
        while True:
            page=page+1
            print(shop_url_1+"/api/2019-04/customers/search.json?tag=NPAPI&limit=250&page="+str(page))
            data1 = requests.get(shop_url_1+"/api/2019-04/customers/search.json?tag=NPAPI&limit=250&page="+str(page),headers=headers).json()
            try:
                resources.extend(data1['customers'])
                if len(resources)<250:
                    break
            except:
                break
        return resources
    except Exception as e:
        print("error",e)
        pass
def get_users_data(count,last__run_time):
    resources = []
    if count > 0:
        print("----Geting count------")
        for page in range(1, ((count-1) // 250) + 2):
            try:
                print(page)
                #print(shop_url_1+"/api/2019-04/customers/search.json?limit=250&page="+str(page)+"&created_at_min="+last__run_time)
                    #data1 = requests.get(shop_url_1+"/api/2019-04/customers/search.json?limit=250&page="+str(page)+"&created_at_min="+last__run_time,headers=headers) #?created_at_min=")
                data1 = requests.get(shop_url_1+"/api/2019-04/customers/search.json?tag=NPAPI&limit=250&page="+str(page),headers=headers) #?created_at_min=")
                data1=data1.json()
                    # print("type of",type(data1))
                #print(len(data1['customers']))
                #sys.exit()
                resources.extend(data1['customers'])
            except:
                #page=page-1
                print("page minus one")
                # break
    return resources
def remove_extra_details(users_datas):
    print("------in remove section------")
    filter_tag_data=[]
    # print(users_datas['customers']) 
    for uses_data in  users_datas:
        # print(uses_data['tags'])
        if uses_data['tags']!='':
            # print(uses_data['tags'])
            # if uses_data['tags'].split('-')[0]=='20' or uses_data['tags'].split('-')[0]=='22' or uses_data['tags'].split('-')[0]=='23' or uses_data['tags'].split('-')[0]=='30':
            if "NPAPI" in uses_data['tags']:
                print("tgas==============")
                print(uses_data['tags'])
                filter_tag_data.append(uses_data)

    return filter_tag_data   
        # break
def update_metfield(data,sage_data):
    ikk=0
    try:
        customer = shopify.Customer.find(data['id'])
        metafields = customer.metafields()
        if sage_data['AddressLine2']==None:
            sage_data_AddressLine2='-'
        else:
            sage_data_AddressLine2=sage_data['AddressLine2']
        customer.add_metafield(shopify.Metafield({
                "key":"AddressLine2",
                "value": sage_data_AddressLine2,
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['AddressLine3']==None:
            sage_data_AddressLine3='-'
        else:
            sage_data_AddressLine3=sage_data['AddressLine3']
        customer.add_metafield(shopify.Metafield({
                "key":"AddressLine3",
                "value": sage_data_AddressLine3,
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['ARDivisionNo']==None:
            sage_data_ARDivisionNo='-'
        else:
            sage_data_ARDivisionNo=sage_data['ARDivisionNo']
        customer.add_metafield(shopify.Metafield({
                "key":"ARDivisionNo",
                "value":sage_data_ARDivisionNo,
                "value_type": "string",
                "namespace": "SAGE",
            }))
        print("one compelted")
        if sage_data['CustomerDiscountRate']==None:
            sage_data_CustomerDiscountRate='-'
        else:
            sage_data_CustomerDiscountRate=sage_data['CustomerDiscountRate']
        customer.add_metafield(shopify.Metafield({
                "key":"CustomerDiscountRate",
                "value":str(sage_data_CustomerDiscountRate),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['CustomerNo']==None:
            sage_data_CustomerNo='-'
        else:
            sage_data_CustomerNo=sage_data['CustomerNo']
        customer.add_metafield(shopify.Metafield({
                "key":"CustomerNo",
                "value":str(sage_data_CustomerNo),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['CustomerStatus']==None:
            sage_data_CustomerStatus='-'
        else:
            sage_data_CustomerStatus=sage_data['CustomerStatus']
        customer.add_metafield(shopify.Metafield({
                "key":"CustomerStatus",
                "value":str(sage_data_CustomerStatus),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['DateCreated']==None:
            sage_data_DateCreated='-'
        else:
            sage_data_DateCreated=sage_data['DateCreated']
        customer.add_metafield(shopify.Metafield({
                "key":"DateCreated",
                "value":str(sage_data_DateCreated),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['DateUpdated']==None:
            sage_data_DateUpdated='-'
        else:
            sage_data_DateUpdated=sage_data['DateUpdated']
        customer.add_metafield(shopify.Metafield({
                "key":"DateUpdated",
                "value":str(sage_data_DateUpdated),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        print("Two compelted")
        if sage_data['DefaultPaymentType']==None:
            sage_data_DefaultPaymentType='-'
        else:
            sage_data_DefaultPaymentType=sage_data['DefaultPaymentType']
        customer.add_metafield(shopify.Metafield({
                "key":"DefaultPaymentType",
                "value":str(sage_data_DefaultPaymentType),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        time.sleep(0.5)
        if sage_data['FaxNo']==None:
            sage_data_FaxNo='-'
        else:
            sage_data_FaxNo=sage_data['FaxNo']
        customer.add_metafield(shopify.Metafield({
                "key":"FaxNo",
                "value":str(sage_data_FaxNo),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['PriceLevel']==None:
            sage_data_PriceLevel='-'
        else:
            sage_data_PriceLevel=sage_data['PriceLevel']
        customer.add_metafield(shopify.Metafield({
                "key":"PriceLevel",
                "value":str(sage_data_PriceLevel),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['ResidentialAddress']==None:
            ResidentialAddress='-'
        else:
            ResidentialAddress=sage_data['ResidentialAddress']
        customer.add_metafield(shopify.Metafield({
                "key":"ResidentialAddress",
                "value":str(ResidentialAddress),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['SalespersonDivisionNo']==None:
            SalespersonDivisionNo='-'
        else:
            SalespersonDivisionNo=sage_data['SalespersonDivisionNo']
        customer.add_metafield(shopify.Metafield({
                "key":"SalespersonDivisionNo",
                "value":str(SalespersonDivisionNo),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['SalespersonNo']==None:
            SalespersonNo='-'
        else:
            SalespersonNo=sage_data['SalespersonNo']
        customer.add_metafield(shopify.Metafield({
                "key":"SalespersonNo",
                "value":str(SalespersonNo),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['ServiceChargeRate']==None:
            ServiceChargeRate='-'
        else:
            ServiceChargeRate=sage_data['ServiceChargeRate']
        customer.add_metafield(shopify.Metafield({
                "key":"ServiceChargeRate",
                "value":str(ServiceChargeRate),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['ShipMethod']==None:
            ShipMethod='-'
        else:
            ShipMethod=sage_data['ShipMethod']
        customer.add_metafield(shopify.Metafield({
                "key":"ShipMethod",
                "value":str(ShipMethod),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['TaxExemptNo']==None:
            TaxExemptNo='-'
        else:
            TaxExemptNo=sage_data['TaxExemptNo']
        customer.add_metafield(shopify.Metafield({
                "key":"TaxExemptNo",
                "value":str(TaxExemptNo),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        time.sleep(0.5)
        if sage_data['TaxSchedule']==None:
            TaxSchedule='-'
        else:
            TaxSchedule=sage_data['TaxSchedule']
        customer.add_metafield(shopify.Metafield({
                "key":"TaxSchedule",
                "value":str(TaxSchedule),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['TelephoneExt']==None:
            TelephoneExt='-'
        else:
            TelephoneExt=sage_data['TelephoneExt']
        customer.add_metafield(shopify.Metafield({
                "key":"TelephoneExt",
                "value":str(TelephoneExt),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['TemporaryCustomer']==None:
            TemporaryCustomer='-'
        else:
            TemporaryCustomer=sage_data['TemporaryCustomer']
        customer.add_metafield(shopify.Metafield({
                "key":"TemporaryCustomer",
                "value":str(TemporaryCustomer),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['TermsCode']==None:
            TermsCode='-'
        else:
            TermsCode=sage_data['TermsCode']
        customer.add_metafield(shopify.Metafield({
                "key":"TermsCode",
                "value":str(TermsCode),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['UDF_CUSTOMER_TYPE']==None:
            UDF_CUSTOMER_TYPE='-'
        else:
            UDF_CUSTOMER_TYPE=sage_data['UDF_CUSTOMER_TYPE']
        customer.add_metafield(shopify.Metafield({
                "key":"UDF_CUSTOMER_TYPE",
                "value":str(UDF_CUSTOMER_TYPE),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['UDF_DDFN']==None:
            UDF_DDFN='-'
        else:
            UDF_DDFN=sage_data['UDF_DDFN']
        customer.add_metafield(shopify.Metafield({
                "key":"UDF_DDFN",
                "value":str(UDF_DDFN),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        #time.sleep(0.5)
        if sage_data['UDF_WSP_WEB_ENABLED']==None:
            UDF_WSP_WEB_ENABLED='-'
        else:
            UDF_WSP_WEB_ENABLED=sage_data['UDF_WSP_WEB_ENABLED']
        customer.add_metafield(shopify.Metafield({
                "key":"UDF_WSP_WEB_ENABLED",
                "value":str(UDF_WSP_WEB_ENABLED),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['URLAddress']==None:
            URLAddress='None'
        else:
            URLAddress=sage_data['URLAddress']
        customer.add_metafield(shopify.Metafield({
                "key":"URLAddress",
                "value":str(URLAddress),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        if sage_data['UserCreatedKey']==None:
            UserCreatedKey='-'
        else:
            UserCreatedKey=sage_data['UserCreatedKey']
        customer.add_metafield(shopify.Metafield({
                "key":"UserCreatedKey",
                "value":str(UserCreatedKey),
                "value_type": "string",
                "namespace": "SAGE",
            }))
        print("last one")
        if sage_data['UserUpdatedKey']==None:
            UserUpdatedKey='-'
        else:
            UserUpdatedKey=sage_data['UserUpdatedKey']
        customer.add_metafield(shopify.Metafield({
                "key":"UserUpdatedKey",
                "value":str(UserUpdatedKey),
                "value_type": "string",
                "namespace": "SAGE",
            }))
       
        try:
            data_tags=data['tags'].split(',')
            final_tag=[]
            for data_tag in data_tags:
                if 'NPAPI' in data_tag:
                    continue
                final_tag.append(data_tag)
            data_tags_string = ','.join(final_tag)
            print("data_tags_string==",data_tags_string)
        except Exception as e:
            print(e)
        try:
            # try:
            #     pricelevel=taxschedule=customer_acc=billing_address1=billing_address2=billing_city=billing_state=billing_zip=billing_country=''
            #     company_name=bill_address=c_email=billing_phone=termscode=''
            #     bill_address=billing_address1+billing_address2+billing_city+billing_state+billing_zip+billing_country
            #     try:
            #         if sage_data['CustomerNo']==None:
            #             customer_acc='-'
            #         else:
            #             customer_acc=sage_data['CustomerNo']
            #     except:
            #         pass
            #     billing_info='Sage Billing Info \nCustomer Account #: '+str(customer_acc)+'\nCustomer Name: ' +str(company_name)+'\nCustomer Address:' +bill_address+'\nSales Person: - \nCustomer Email: ' +c_email+' \nCustomer Phone :' +billing_phone+' \nTermsCode: '+str(termscode)+'\nPrimary Contact: -\nTAX Schedule: '+str(taxschedule)+'\nPrice Level: '+pricelevel+' \n'

            # except:
            #     pass

            c = shopify.Customer.find(data['id'])
            c.tags = data_tags_string
            # c.note = billing_info
            c.save()
            print("update new tags ")
        except:
            pass
        print('-------- updated metafield in shopify -------')
        sync_updatenotes(data['id'])
    except Exception as e:
        time.sleep(1)
        print("Error in  metafield update",e)
        update_metfield(data,sage_data)
        
    
    
def email_query_get_data(email,data):
    print("email_query_get_data---email-",email)
    conn = pyodbc.connect("DSN=xxxxx;UID=xxxx;PWD=xxxxxxxxxx;",autocommit=True)
    cursor =conn.cursor()
    cursor.execute("SELECT * from ar_customer where EmailAddress='"+email+"'")
    results=cursor.fetchall()
    columname=[]
    print("this is getting column from sage",len(results))
    if len(results)==1:
        for row in cursor.columns(table='ar_customer'):
            columname.append(row.column_name)
            #print (row.column_name)
        values=[]
        for re_i in results[0]:
            values.append(re_i)
        sage_data = dict(zip(columname, values))
        #print("shopify data===>>",data)
        #print("sage_data=====>>",sage_data)
        update_metfield(data,sage_data)
      
def call_update_and_sage(filter_data):
    print("call function update and sage call ")
    for filter_i in filter_data:
        
        #print("this is data==>>")
        #print(filter_i)
        email_query_get_data(filter_i['email'],filter_i)
    


if __name__ == "__main__":
    # filename_csv=sys.argv[1]
    logging.basicConfig(filename="mirrormate.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='a')
    logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    start_time = time.time()
    logger.info("Start Time :{}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    formattime = "%Y-%m-%dT%H:%M:%S"
    now_time = datetime.now(timezone('US/Eastern')) #- timedelta(days=7)
    current_runtime = now_time.strftime(formattime)
    users_datas_2=get_users_data_2()
    print(len(users_datas_2))
    # print(users_datas_2)
    # filter_data=remove_extra_details(users_datas)
    debug_var=call_update_and_sage(users_datas_2)
    
    # with open("users_datas.txt", "w") as output:
    #     output.write(str(debug_var))
    # -----------------------------------
    # products = get_all_resources(shopify.customers)
    
    # print("lenght ==",len(products))R
    # count=get_count()
    # count.text
    # print(count.json()['customers'])
    # print(count.text)
    # ---------------------------------
    end_time =time.time()
    print("Total Time taken to get results:{}".format(end_time-start_time))
    logger.info("End Time :{}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
        
        # p = Pool(int(sys.argv[3]))
        # p.map(get_data, urlList)
                        

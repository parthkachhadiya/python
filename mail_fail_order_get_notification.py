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
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

headers = {"Accept": "application/json", "Content-Type": "application/json"}
API_KEY = 'xxxxxxxxxxxxxxxxxx'
PASSWORD = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
shop_url_1 = "https://%s:%s@mirrormatellc.myshopify.com/admin" % (API_KEY, PASSWORD)
shopify.ShopifyResource.set_site(shop_url_1)
sendgridapikey = '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'
print(shop_url_1+"/api/2020-04/orders/count.json?status=any")
order_count = requests.get(shop_url_1+"/api/2020-04/orders/count.json?status=any",headers=headers).json()['count']
print("count===",order_count)
count_tags_failuler=0
count_tags_blank=0
fauiler_tag_list=[]
blank_tag_list=[]
for i in range(1,int(order_count/250)):
    for k in range(1,15):
        customer_count = requests.get(shop_url_1+"/orders.json?limit=250&status=any&page="+str(k),headers=headers) #?created_at_min=")
        # print("----------------------------------")
        # print(customer_count.json()['orders'])
        for i in customer_count.json()['orders']:
            if  i['tags']=="Success":
                continue
                # print(i)
                # sys.exit()
            elif "Failure" in i['tags']:
                # customer_count = requests.get(shop_url_1+"/orders/.json?limit=250&status=any&page="+str(k),headers=headers)
                count_tags_failuler=count_tags_failuler+1
                # print("problem in tag")
                print("id====>>>",i['id'])
                print("tag that have ===>>",i['tags'])
                print("tag that number ===>>",i['number'])
                fauiler_tag_list.append(i['number'])
            else:
                print(shop_url_1+"/api/2020-04/orders.json?ids="+str(i['id']))
                order_json = requests.get(shop_url_1+"/api/2020-04/orders.json?ids="+str(i['id']),headers=headers)
                print(order_json.json())
                sys.exit()
                count_tags_blank=count_tags_blank+1
                # print("problem in tag")
                print("id====>>>",i['id'])
                print("tag that have ===>>",i['tags'])
                print("tag that number ===>>",i['number'])
                blank_tag_list.append(i['number'])
        time.sleep(1)

# shop_url_1+"/admin/api/2020-04/orders/count.json")

sys.exit()

from selenium import webdriver
from seleniumwire import webdriver
import time
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import sys
import csv
import random
from datetime import datetime,timedelta
from pytz import timezone
from datetime import datetime
import datetime
from multiprocessing import Process, Pool
import multiprocessing
import datetime
import logging
import json
import mysql.connector
import re
import yaml
import os
from sys import exit
from multiprocessing import Process, Pool
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
print("db change")
# from datetime import datetime
def random_time_picker():
    return random.uniform(0.3,0.85)
def random_proxy_picker():
    with open("/home/hitul/google_trends/main/proxies.csv") as f:
        reader = csv.reader(f)
        chosen_row = random.choice(list(reader))
    return chosen_row[0]
def random_height_scroll():
    li_heights=[]
    for i in range(100,250):
        li_heights.append(i)
    return random.choice(li_heights)

def get_url_db():
    print("gtrends_urls")
    urls=[]
    try:
        db_connection = mysql.connector.connect(
        host="78.46.xxxx.xxx",
        user="xxxxx",
        passwd="xxxx",
        database="keywords"
        #py_wordpress
        )
        db_cursor = db_connection.cursor(buffered=True)
        try:
            query=("SELECT * FROM gtrends_urls WHERE STATUS='False' LIMIT 1")        
            db_cursor.execute(query)
            myresult = db_cursor.fetchall() 
        except Exception as e:
            print(e)
            pass
        db_cursor.close()
        db_connection.close()
    except Exception as e:
        print("database Error: ",e)
        pass
    return myresult
def found_loadmore(page_source):
    print("inside load mor bs4s----")
    soup = BeautifulSoup(page_source, 'lxml')
    
    load_more_button = soup.find("div", {"class": "feed-load-more-button"})
    try:
        print("load_more_button===>>",load_more_button.get_text())
        return True
    except:
        print("except false")
        return False
def db_status(url):
    try:
        db_connection = mysql.connector.connect(
        host="78.46.xxx.xxxx",
        user="xxxx",
        passwd="xxxxx",
        database="keywords" 
        )
        db_cursor = db_connection.cursor(buffered=True)
        
        try:
            query="UPDATE gtrends_urls set status=True where url='"+url+"'"    
            print(query)    
            db_cursor.execute(query) 
            db_connection.commit()
        except Exception as e:
            # print("Err: in db: ",e)
            pass
        db_cursor.close()
        db_connection.close()
    except Exception as e:
        db_cursor.close()
        db_connection.close()
        print("database Error: ",e)
        pass
    return True


def insert_data(i):
    try:
        db_connection = mysql.connector.connect(
                host="78.46.xxxx.xxx",
                user="xxxx",
                passwd="xxxxx",
                database="xxxx" 
                )
        db_cursor = db_connection.cursor(buffered=True)
        # for i in data:
        try:        
            try:
                query=('insert into gtrends_data (query,value,date,country,category,token) VALUES(%s,%s,%s,%s,%s,%s)')        
                db_cursor.execute(query,(i[0],i[1],i[2],i[3],i[4],i[5])) 
                db_connection.commit()
            except Exception as e:
                print("Err: in db: ",e)
                db_connection.rollback()
                pass
        except:
            pass
        db_cursor.close()
        db_connection.close()
    except Exception as e:
        db_cursor.close()
        db_connection.close()
        print("database Error: ",e)
        pass


def browser(url):
    try:
        print("working on this url--->>>,",url)
        host_port=random_proxy_picker()
        print("this is proxy==>>",host_port)
        options = {
            'proxy': {
                'http': 'http://@'+str(host_port),
                'https': 'https://@'+str(host_port),
                # 'http': 'http://username:password@host:port',
                # 'https': 'https://username:password@host:port',
                'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
                }
            }
        
        display = Display(visible=0, size=(1080, 720))
        display.start()
        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        driver=webdriver.Firefox(seleniumwire_options=options)
        driver.maximize_window()
        # print("here -1")
        driver.set_page_load_timeout(150)
        driver.get(url)
        print("here 1")
        time.sleep(random_time_picker())
        # print("here 2")
        driver.execute_script("window.scrollTo(0, "+str(random_height_scroll())+")") 
        # print("here 3")
        time.sleep(random_time_picker())
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # print("here 4")
        time.sleep(random_time_picker())
        time.sleep(random_time_picker())
        time.sleep(random_time_picker())
        # print("here 5")
        page_source_bs = driver.page_source
        soup = BeautifulSoup(page_source_bs, 'lxml')
        # file = open("testfile.txt","w") 
        # file.write(soup.text)
        print("this is length of soup",len(soup.text))
        if "are not available for this" in soup.text:
            print("NO result")
            re=db_status(url)
            print(re)
            return False
        if len(soup.text)>50000:
            flag=1 
            re=db_status(url)
            print(re)
        else:
            print("Retring...")
            # display.close()
            driver.close()
            driver.quit()
            display.stop()
            # driver.close()
            browser(url)
            flag=0    
        ch=0
        while True:
            try:
                ch=ch+1
                time.sleep(2.52)
                page_source_bs = driver.page_source
                result=found_loadmore(page_source_bs)
                print("result",result)
                if result:
                    print("click load more")
                    time.sleep(random_time_picker())
                    driver.execute_script("window.scrollTo(0, "+str(random_height_scroll())+")") 
                    # driver.find_element_by_css_selector('.feed-load-more-button').click()
                    time.sleep(random_time_picker())
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(random_time_picker())
                    time.sleep(random_time_picker())
                    driver.find_element_by_css_selector('.feed-load-more-button').click()
                    time.sleep(2.52)
                else:
                    page_source_bs = driver.page_source
                    print("get page source")
                    break
            except:
                time.sleep(random_time_picker())
            # if ch==2:
            #     time.sleep(2.52)
            #     break
            # --commented
        res_ajax=[]
        res_urls=[]
        res_tokens=[]
        time.sleep(5)
        result_list=[]
        for request in driver.requests:
            if request.response:
                if "/widgetdata/relatedqueries" in str(request.path):
                    sub_result_list=[]
                    try:
                        url_1=request.path
                        token=url_1.split('&token=')[1]
                        res_tokens.append(token)
                    except Exception as e:
                        print("err token",e)
                        pass
                    try:
                        result_list.append(str(request.response.body))
                    except:
                        sub_result_list=[]
                        pass
                    res_urls.append(str(request.path))
                    res_ajax.append(str(request.response.body))
                    # print("-------------------------------------------------")
                    # print(len(res_ajax))
                    # print(len(res_tokens))
                    # print("-----------------------------------------")
        print("database ====")
        try:
            date=datetime.datetime.today()
            date=str(date).split()[0]
            location=url.split('&category=')[0].split('?geo=')[1].upper()
            if "GB" in location:
                location="UK"
            if "GB" in location:
                location="UK"
            cat=url.split('&category=')[1]
            print("cat split=",cat)
            if cat=="b":
                cat="Business"
            if  cat=='e':
                cat="Entertainment"
            if cat=='m':
                cat="Health"
            if cat=='t':
                cat="Sci/Tech"
            if cat=='s':
                cat="Sports"
            if cat=="h":
                cat="Top Stories"
            print("cat=====>>",cat)
            print("location=====>>",location)
            data=[]
            k=0
            for string in res_ajax:
                try :
                    string=string[10:]
                    string=string[:-1]
                    # string = string.encode("utf-8")
                    string=string.replace("\'t","")
                    string=string.replace("\t","")
                    string=string.replace('\\',"")
                    string_y=yaml.load(string)
                    # print("string",string_y)
                    # print("type of string",type(string_y))

                    for i in  string_y['default']['queries']:
                        sub_data=[i['query'],i['value'],date,location,cat,res_tokens[k]]
                        data.append(sub_data)
                except:
                    pass
                k=k+1
            try:
                # print(data)
                print("database operation----")
                p = Pool(15)
                p.map(insert_data, data)
                # try:
                #     db_connection = mysql.connector.connect(
                #             host="78.46.165.80",
                #             user="gtrends",
                #             passwd="ahgqDp5pQNRKHM4Q",
                #             database="keywords" 
                #             )
                #     db_cursor = db_connection.cursor(buffered=True)
                #     for i in data:
                #         try:        
                #             try:
                #                 query=('insert into gtrends_data (query,value,date,country,category,token) VALUES(%s,%s,%s,%s,%s,%s)')        
                #                 db_cursor.execute(query,(i[0],i[1],i[2],i[3],i[4],i[5])) 
                #                 db_connection.commit()
                #             except Exception as e:
                #                 print("Err: in db: ",e)
                #                 db_connection.rollback()
                #                 pass
                #         except:
                #             pass
                #     db_cursor.close()
                #     db_connection.close()
                # except Exception as e:
                #     db_cursor.close()
                #     db_connection.close()
                #     print("database Error: ",e)
                #     pass
                print("DB Done")
                driver.close()
                driver.quit()
                display.stop()
                # os.system("pkill -9 Xvfb")
                # os.system("pkill -9 firefox")
                print ("driver closed")
                exit(0)
                # return True
            except Exception as e:
                print("database Error: ",e)
                pass      
        except Exception as e:
            print("err: Data format and data base",e)
            # return True
            

    # except Exception as e:
    #     print("err data format:",e)
    #     driver.close()
    #     driver.quit()
    #     display.stop()
    #     # return True
        
        
    except Exception as e:
        try:
            print("Err browser",e)
            driver.close()
            driver.quit()
            display.stop()
            
            # time.sleep(random_time_picker())
            
            browser(url)
            
        except:
            return False
            pass

            # return True
            # driver.close()
    print("return true")
    return True



    
if __name__ == "__main__":
    # filename_csv=sys.argv[1]
    logging.basicConfig(filename="sync_google_treads.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='a')
    logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(     )s - %(message)s','%m-%d %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    start_time = time.time()
    logger.info("Start Time :{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print("------------Start-------------")
    urls=get_url_db()
    # print(urls[0][1])
    if len(urls)==0:
        print("------------------script on hold------------------")
        time.sleep(1800)
    for url in urls:
        re=browser(url[1])
        print(re)
    print("-------------END-------------")
    # print(users_datas[0])
    # os.system("pkill -9 Xvfb")
    # os.system("pkill -9 firefox")
    # os.system("pkill -9 Xvfb")
    end_time =time.time()
    print("Total Time taken to get results:{}".format(end_time-start_time))
    logger.info("End Time :{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    

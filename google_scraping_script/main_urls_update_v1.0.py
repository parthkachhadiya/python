import schedule
import time
import mysql.connector
import datetime
import logging
import os
def job():
    try:
        logging.basicConfig(filename="run_urls_times.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='a')
        logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        start_time = time.time()
        logger.info("Start Time :{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        try:
            os.remove("sync_google_treads.log")
        except:
            pass
        db_connection = mysql.connector.connect(
        host="78.xxx.xxx.xx",
        user="xxx",
        passwd="xxx",
        database="xxxxxx" 
        )
        db_cursor = db_connection.cursor(buffered=True)
        
        try:
            query="UPDATE gtrends_urls set status=False"    
            print(query)    
            db_cursor.execute(query) 
            db_connection.commit()
        except Exception as e:
            print("Err: in db: ",e)
            pass
        db_cursor.close()
        db_connection.close()
        end_time =time.time()
        print("Total Time taken to get results:{}".format(end_time-start_time))
        logger.info("End Time :{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    except Exception as e:
        db_cursor.close()
        db_connection.close()
        print("database Error: ",e)
        pass

# schedule.every(10).seconds.do(job)
schedule.every().day.at("04:55").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
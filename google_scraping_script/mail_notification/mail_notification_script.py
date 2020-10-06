import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
import mysql.connector
import datetime
import logging
import os
def mail(content,content_1,content_2):
    try:
        mail_content = '''Hello Team,
        Here less count or script will stop 
        Content Missing: '''+str(content_2)+'''
        Count: '''+str(content_1)+'''
        Query for that: '''+str(content)+'''
        Date and time: '''+str(datetime.datetime.today())+'''
        Thank You.
        '''
        #The mail addresses and password
        sender_address = 'parth.work9898@gmail.com'
        sender_pass = '9898356409'
        receiver_address = 'parth.work9898@gmail.com'
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        # message['Cc'] = 'hitul@genextwebs.com'
        message['Subject'] = 'Google Treands Mail script less count'   #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.ehlo()
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('---------------------Mail Sent-------------------- 1')

        #The mail addresses and password
        sender_address = 'parth.xxxxxx@xxxxx.com'
        sender_pass = 'xxxxxxxxxxxxxxxx'
        receiver_address = 'xxxx@xxx.com'
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        # message['Cc'] = 'xxxx@xxxxx.com'
        message['Subject'] = 'Google Treands Mail script less count'   #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.ehlo()
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('---------------------Mail Sent-------------------- 2')
    except Exception as e:
        print("mail sent err:",e)
        pass

def job():
    
    urls=[]
    try:
        print("start --")
        date=datetime.datetime.today()
        date=str(date).split()[0]
        print("run for date",date)
        # date='2020-05-11'
        db_connection = mysql.connector.connect(
        host="78.46.xxxx.xxx",
        user="xxx",
        passwd="xxxx",
        database="xxx"
        #py_wordpress
        )
        db_cursor = db_connection.cursor(buffered=True)
        try:
            count=0
            query=("SELECT count(*) FROM gtrends_data WHERE date='"+date+"'")     
            # print(query)   
            db_cursor.execute(query)
            myresult_count = db_cursor.fetchall() 
            count=myresult_count[0][0]
            query1=("SELECT COUNT(DISTINCT country) FROM `gtrends_data` WHERE date='"+date+"'")     
            # print(query1)   
            db_cursor.execute(query1)
            myresult_count_county = db_cursor.fetchall() 
            query2=("SELECT COUNT(DISTINCT category) FROM `gtrends_data` WHERE date='"+date+"'")     
            # print(query1)   
            db_cursor.execute(query2)
            myresult_count_category = db_cursor.fetchall() 
            if myresult_count_category[0][0]!=7:
                mail(query2,myresult_count_county[0][0],"Category missing")
            if myresult_count_county[0][0]!=6:
                mail(query1,myresult_count_county[0][0],"Country  missing")
            if count<40000:
                print("count are less than 40000")
                mail(query,count,"Overall count less")
        except Exception as e:
            print(e)
            pass
        db_cursor.close()
        db_connection.close()
    except Exception as e:
        print("database Error: ",e)
        pass

# schedule.every(10).seconds.do(job)
schedule.every().day.at("15:55").do(job)
# job()

while True:
    schedule.run_pending()
    time.sleep(1)  
# mail("this is ", "this is demo")
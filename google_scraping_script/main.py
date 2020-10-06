import subprocess
import time
import os
from datetime import datetime
import random
import numpy as np
list_time=np.arange(10,100, 0.5).tolist()
while True:
    try:
        print("Started at :{}".format(datetime.now()))
        subprocess.call('python3 sync_db_google_trends.py',shell=True)
        # time_sleep_timer=random.choice(list_time)
        print("time sleep for :",time_sleep_timer)
        # os.system("python3 sync_db_google_trends.py")
        # time.sleep(time_sleep_timer)
        
        os.system("pkill -9 Xvfb")
        os.system("pkill -9 firefox")
        os.system("pkill -9 phantomjs")
        os.system("pkill -9 mysql")
        
        print("Finshed at :{}".format(datetime.now()))
        # time.sleep(200)
    except:
        pass
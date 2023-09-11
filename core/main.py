
# Schedule Library imported
import schedule
import time
 
from utils.log import Logger
from datetime import datetime
from utils.support import Support
from utils import epoch

# def service():
#     logger = Logger()
#     # support = Support(logger, spidey_user="anhnt376", start=epoch.create_timestamp(7,19,50), duration=4, mode="debug")
#     support = Support(logger)
#     support.login()

if __name__ == "__main__": 
    # service()
    
    with open('/core/samples/sample1.txt', 'r') as file:
        Lines = file.readlines()
        file.close()
        
    
    support = Support(Logger())
        
    
    for line in Lines:
        support.login(mail=line, password="Soctrang@123")
    
    # epoch.create_timestamp(9, 0)
    # print(epoch.create_timestamp(7,1))
    # print(epoch.get_month())
    
    # schedule.every().day.at("17:00").do(service)
    
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60) # wait 15 minute
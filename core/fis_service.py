from utils.log import Logger
from datetime import datetime
from utils.support import Support

def service():
    logger = Logger()
    support = Support(logger, spidey_user="tuanlda@fpt.com.vn", start=1693764000.01, duration=4)
    support.login()

if __name__ == "__main__":     
    service()
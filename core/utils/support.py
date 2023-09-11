import os
import time 
import cv2
import sys
import traceback
import asyncio

sys.path.append("/core/utils/")
sys.path.append("/core/database/")

from utils.log import Logger
from utils.otp import OTP
from utils.chatbot import ChatBot
# from log import Logger # for testing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from helper import Helper

USER_AGENT = os.getenv("USER_AGENT")
SPIDEY_URL = os.getenv("SPIDEY_SOC")

DVC_URL = "https://10.14.132.47:45058/"

MIN12 = 5
MIN5 = 5*60
MIN10 = 10*60
MIN15 = 15*60

BROWSER_OPTIONS = webdriver.ChromeOptions()      
BROWSER_OPTIONS.add_argument('--headless')
BROWSER_OPTIONS.add_argument('ignore-certificate-errors')
BROWSER_OPTIONS.add_argument("--start-maximized")
BROWSER_OPTIONS.add_argument(f'user-agent={USER_AGENT}')
BROWSER_OPTIONS.add_argument("--window-size=1920,1080")
BROWSER_OPTIONS.add_argument('--allow-running-insecure-content')
BROWSER_OPTIONS.add_argument("--disable-extensions")
BROWSER_OPTIONS.add_argument("--proxy-server='direct://'")
BROWSER_OPTIONS.add_argument("--proxy-bypass-list=*")
BROWSER_OPTIONS.add_argument("--start-maximized")
BROWSER_OPTIONS.add_argument('--disable-gpu')
BROWSER_OPTIONS.add_argument('--disable-dev-shm-usage')
BROWSER_OPTIONS.add_argument('--no-sandbox')

class Support():
    """ 
    A class to take a screenshot of a webpage after logging in with provided username and password
    
    """
    def __init__(self, logger,  mode: str = "info"):

        self.logger = logger
        self.wait = 3
        self.driver = webdriver.Chrome(options=BROWSER_OPTIONS)
        self.mode = mode
        self.chatbot = ChatBot(logger)
        
    def login(self, mail: str, password: str):
        f = open("Default_pass.txt", "a")
        try: 
            self.driver.get(DVC_URL) # Navigating to the given URL.

            # Get user input -> enter username
            # element_name = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.ID,"usernameUserInput")))
            element_name = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.ID,"username")))
            element_name.send_keys(mail)
            
            # Get password input -> enter password
            # element_pass = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.ID,"password")))
            element_pass = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.ID,"password")))
            element_pass.send_keys(password)
            
            self.driver.save_screenshot("/core/media/auto/fill_login.png")
            
            element_login = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.CLASS_NAME,"ZLoginButton")))
            element_login.click()
            
            if WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.CLASS_NAME,"ZWidgetTitle"))):
                self.logger.log_message(f"Thành công: {mail}", "info")
                self.driver.save_screenshot(f"/core/media/auto/login_status-{mail}.png")
                f.write(mail)
            
            # self.driver.close()
                
        except Exception as error:
            # self.logger.log_message(error, "error")
            self.logger.log_message(f"Logging error: {mail}", "error")
            self.driver.save_screenshot("/core/media/auto/error.png")
            # self.driver.close()
        f.close()
    
if __name__ == "__main__":  
    
    pass 
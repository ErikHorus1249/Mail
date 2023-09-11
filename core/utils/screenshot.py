import os
import time 
import cv2
import sys
import traceback

sys.path.append("/core/utils/")

from utils.log import Logger
# from log import Logger # for testing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


USER_AGENT = os.getenv("USER_AGENT")
MDR_HOST = os.getenv("MDR_HOST")
MDR_PORT = os.getenv("MDR_PORT")
SPIDEY_URL = os.getenv("SPIDEY_URL")
HELION_URL = os.getenv("HELION_URL")

MDR_USER = os.getenv("MDR_USER")
MDR_PASSWD = os.getenv("MDR_PASSWD")
SPIDEY_USER = os.getenv("SPIDEY_USER")
SPIDEY_PASSWD = os.getenv("SPIDEY_PASSWD")
HELION_USER = os.getenv("HELION_USER")
HELION_PASSWD = os.getenv("HELION_PASSWD")
KIBANA_HOST = os.getenv("KIBANA_HOST")
KIBANA_USER = os.getenv("KIBANA_USER")
KIBANA_PASS = os.getenv("KIBANA_PASS")
KIBANA_PERIOD = os.getenv("KIBANA_PERIOD")
SPLUNK_HOST = os.getenv("SPLUNK_HOST")
SPLUNK_PORT = os.getenv("SPLUNK_PORT")
SPLUNK_USER = os.getenv("SPLUNK_USER")
SPLUNK_PASS = os.getenv("SPLUNK_PASS")

IMAGE_DIR = os.getenv("FINAL_REPORT")

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

class TakeWebPriScr():
    """ 
    A class to take a screenshot of a webpage after logging in with provided username and password
    
    """
    def __init__(self, logger: Logger, wait_time: int =120, image_dir: str = IMAGE_DIR):
        """
        Constructs the necessary attributes for TakeWebPriScr object.
        
        Args:
        url (str): URL for the webpage.
        username(str): Username for logging in.
        password(str): Password for logging in.
        image_path(str): Path to save the screenshot.
        wait_time(int): Time to wait for elements to load. Default is 120 seconds.
        
        """
        
        self.logger = logger
        self.wait = wait_time
        self.spd_user = SPIDEY_USER
        self.spd_passwd = SPIDEY_PASSWD
        self.mdr_user = MDR_USER
        self.mdr_passwd = MDR_PASSWD
        self.helion_user = HELION_USER
        self.helion_passwd = HELION_PASSWD
        self.image_dir = image_dir
        
        self.driver = webdriver.Chrome(options=BROWSER_OPTIONS)
        
    def take_screenshot_mdr(self, case: int, offline_sensors: int = 10):
        """
        Logs in to the given webpage and takes a screenshot.
        
        Args:
        user_input(str): HTML input name attribute for entering the username.
        password_input(str): HTML input name attribute for entering the password.
        submit_btn(str): HTML button type attribute for clicking the submit button.
        
        Returns:
        None
        
        """        
        self.logger.log_message("[take_screenshot_mdr] Starting...", "info")
        
        if case == 0:
            FULL_URL_MDR = f"https://{MDR_HOST}:{MDR_PORT}/#/hosts/all?rows={offline_sensors}&sort.col=status&sort.dir=asc&start=0&uninstall=false&uninstalled=false"
            self.image_dir = f"{self.image_dir}CBR_sensor_offline.png"
        elif case == 1:
            FULL_URL_MDR = f"https://{MDR_HOST}:{MDR_PORT}/#/hosts/all?rows={offline_sensors}&sort.col=status&sort.dir=desc&start=0&uninstall=false&uninstalled=false"
            self.image_dir = f"{self.image_dir}CBR_sensor_online.png"
        else:
            self.logger.log_message("Wrong case, must be online or offline", "error")
            return
        
        while self.mdr_user is not None and self.mdr_passwd is not None:
            try:
                print(FULL_URL_MDR)                
                self.driver.get(FULL_URL_MDR) # Navigating to the given URL.
                element_name = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.ID,"username")))
                element_name.send_keys(self.mdr_user)
                element_pass = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.ID, "password")))
                element_pass.send_keys(self.mdr_passwd)
                btn_submit = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.ID, "login")))
                btn_submit.click()
                
                WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.XPATH,"//div[@class='overflow-ellipsis']")))
                
                self.driver.execute_script("document.body.style.zoom='90%'")
                
                html = self.driver.find_element(By.TAG_NAME,'html')
                
                html.send_keys(Keys.END)
                
                
                self.driver.save_screenshot(self.image_dir)  # Saving the screenshot.
                self.driver.quit()  # Closing the driver instance.
                
                if self.crop_image((110, 500), (1080,1920)):
                    self.logger.log_message(f"[take_screenshot_mdr] Finished! saved image:{self.image_dir}", "info")
                
                return self.image_dir
            
            except Exception as error:
                self.logger.log_message(error, "error")
                self.driver.quit()  # Closing the driver instance.
                return    
            
    def take_screenshot_spidey(self):
        
        self.image_dir = f"{self.image_dir}spidey.png"
        self.logger.log_message("[take_screenshot_spidey] Starting...", "info")
        
        while self.spd_user is not None and self.spd_passwd is not None:
            try:

                self.driver.get(SPIDEY_URL) # Navigating to the given URL.
                
                element_name = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.ID,"loginId")))
                element_name.send_keys(self.spd_user)
                element_pass = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.ID,"loginPassword")))
                element_pass.send_keys(self.spd_passwd)
                btn_submit = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.ID,"loginButton")))
                btn_submit.click()

                WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.XPATH,"//span[.='NOC BGT']")))
                
                self.driver.save_screenshot(self.image_dir)  # Saving the screenshot.
                self.driver.quit()  # Closing the driver instance.
                
                self.logger.log_message(f"[take_screenshot_spidey] Finished! saved image:{self.image_dir}", "info")
                
                return self.image_dir
            
            except Exception as error:
                self.logger.log_message(error, "error")
                self.driver.quit()  # Closing the driver instance.
                return
    
    def take_screenshot_helion(self):
        
        self.image_dir = f"{self.image_dir}mGuard-no-log-alert.png"
        self.logger.log_message("[take_screenshot_helion] Starting...", "info")
        
        while self.helion_user is not None and self.helion_passwd is not None:
            try:

                self.driver.get(HELION_URL)  # Navigating to the given URL.
                
                element_name = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.NAME,"username")))
                element_name.send_keys(self.helion_user)
                element_pass = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.NAME,"password")))
                element_pass.send_keys(self.helion_passwd)
                btn_submit = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.XPATH,"//button[@type='submit']")))
                btn_submit.click()

                WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.XPATH,"//div[.='BGT mGuard Alerts No Log (Line)']")))
                
                self.driver.save_screenshot(self.image_dir)  # Saving the screenshot.
                self.driver.quit()  # Closing the driver instance.
                
                self.logger.log_message(f"[take_screenshot_helion] Finished! saved image:{self.image_dir}", "info")
                
                return self.image_dir
            
            except Exception as error:
                self.logger.log_message(error, "error")
                self.driver.quit()  # Closing the driver instance.
                return        
    
    def crop_image(self,start_point: tuple, end_point: tuple) -> bool:
        """Crop and save a region of an image.

        Args:
            import_img (str): Path to the input image file.
            export_img (str): Path to the output cropped image file.
            start_point (tuple): A tuple of two integers representing the starting point (y,x) of the crop.
            end_point (tuple): A tuple of two integers representing the ending point (h,w) of the crop.

        Returns:
            bool: True if the image was successfully cropped and saved, False otherwise.
        """
        if not os.path.isfile(self.image_dir):
            print(f"Error: {self.image_dir} file not found")
            return False
        
        img = cv2.imread(self.image_dir)
        y1, x1 = start_point
        y2, x2 = end_point
        
        if y1 >= y2 or x1 >= x2 or y2 > img.shape[0] or x2 > img.shape[1]:
            print("Error: Invalid cropping points")
            return False

        crop = img[y1:y2, x1:x2]
        
        cv2.imwrite(self.image_dir, crop)
        
        self.logger.log_message(f"[crop_image] Finished! saved image:{self.image_dir}", "info")
        
        return True
    
    def take_screenshot_kibana(self, dashboard):
        
        self.logger.log_message("[take_screenshot_kibana] Starting...", "info")
        
        saved_img = f"{self.image_dir}BGT_{(dashboard['name']).replace(' ', '_')}.png"
        
        # while KIBANA_USER is not None and KIBANA_PASS is not None:
        try:
            kibana_url = f"https://{KIBANA_HOST}:5601/app/dashboards#/view/{dashboard['id']}?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-{KIBANA_PERIOD}m,to:now))&_a=(description:'',filters:!(),fullScreenMode:!f,options:(hidePanelTitles:!f,useMargins:!t),query:(language:kuery,query:''),timeRestore:!f,title:'{dashboard['title']}',viewMode:view)"
            print(kibana_url)
            self.driver.get(kibana_url) # Navigating to the given URL.
            
            element_name = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.NAME,"username")))
            element_name.send_keys(KIBANA_USER)
            element_pass = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.NAME,"password")))
            element_pass.send_keys(KIBANA_PASS)
            btn_submit = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.XPATH,"//button[@type='submit']")))
            btn_submit.click()

            # WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.XPATH,"//div[@class='tvbVisMetric__value--primary']")))
            time.sleep(30)
            
            self.driver.save_screenshot(saved_img)  # Saving the screenshot.
            self.driver.quit()  # Closing the driver instance.
            
            self.logger.log_message(f"[take_screenshot_kibana] Finished! saved image:{saved_img}", "info")
            
            return saved_img
            
        except Exception as error:
            self.logger.log_message(error, "error")
            traceback.print_exc()
            self.driver.quit()  # Closing the driver instance.
            return
    
    def take_screenshot_virustotal(self, item: str, mode: int):
        
        self.image_dir = f"{self.image_dir}mGuard-virustotal.png"
        self.logger.log_message("[take_screenshot_virustotal] Starting...", "info")
        
        # while self.helion_user is not None and self.helion_passwd is not None:
        try:
            # 1: ip 
            # 0: hash 
            if mode == 1:
                VIRUSTOTAL_URL = f"https://www.virustotal.com/gui/ip-address/{item}"
            elif mode == 0:
                VIRUSTOTAL_URL = f"https://www.virustotal.com/gui/file/{item}"
            else:
                return
                
            print(VIRUSTOTAL_URL)
            
            self.driver.get(VIRUSTOTAL_URL)  # Navigating to the given URL.
            
            time.sleep(0.25)
            # WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.XPATH,"//span[@class='engine-name']")))
            
            self.driver.save_screenshot(self.image_dir)  # Saving the screenshot.
            self.driver.quit()  # Closing the driver instance.
            
            self.logger.log_message(f"[take_screenshot_virustotal] Finished! saved image:{self.image_dir}", "info")
            
            return self.image_dir
        
        except Exception as error:
            self.logger.log_message(error, "error")
            self.driver.quit()  # Closing the driver instance.
            return   
    
    def take_screenshot_splunk(self):
        
        self.logger.log_message("[take_screenshot_splunk] Starting...", "info")
        
        self.image_dir = f"{self.image_dir}BGT_Pull-ApexOne-Events-Monitor.png"
        # saved_img = f"{self.image_dir}BGT_Pull-ApexOne-Events-Monitor.png"
        
        try:
            splunk_url = f"https://{SPLUNK_HOST}:{SPLUNK_PORT}/en-GB/app/search/bgt_apexone_monitor"
            
            self.driver.get(splunk_url) # Navigating to the given URL.
            
            element_name = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.NAME,"username")))
            element_name.send_keys(SPLUNK_USER)
            element_pass = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.NAME,"password")))
            element_pass.send_keys(SPLUNK_PASS)
            btn_submit = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.XPATH,"//input[@type='submit']")))
            btn_submit.click()

            # WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.XPATH,"//text[@class='single-result']")))
            time.sleep(5)
            
            self.driver.save_screenshot(self.image_dir)  # Saving the screenshot.
            self.driver.quit()  # Closing the driver instance.
            
            if self.crop_image((80,10), (730, 1920)):
                    self.logger.log_message(f"[take_screenshot_splunk] Finished! saved image:{self.image_dir}", "info")
            
            return self.image_dir
            
        except Exception as error:
            self.logger.log_message(error, "error")
            traceback.print_exc()
            self.driver.quit()  # Closing the driver instance.
            return
 
    def auto_click(self):
            
            self.image_dir = f"{self.image_dir}auto_click.png"
            self.logger.log_message("[Click is enable] Starting...", "info")
            
            # while self.spd_user is not None and self.spd_passwd is not None:
            try:

                # self.driver.get(SPIDEY_URL) # Navigating to the given URL.
                self.driver.get("https://spidey.security.fis.vn/dfir-team/channels/alerts") # Navigating to the given URL.
                
                element_name = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.ID,"loginId")))
                element_name.send_keys(self.spd_user)
                element_pass = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.ID,"loginPassword")))
                element_pass.send_keys(self.spd_passwd)
                btn_submit = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.ID,"loginButton")))
                btn_submit.click()

                # WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.XPATH,"//span[.='NOC BGT']")))
                
                while True:
                    try:
                        WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.XPATH,"//h3[@class='markdown__heading']")))
                        alert = self.driver.find_element(By.CLASS_NAME, 'markdown__heading')
                        self.logger.log_message(alert.text, "info")
                        
                        # self.driver.save_screenshot(self.image_dir)  # Saving the screenshot.
                        # self.logger.log_message(f"[take_screenshot_helion] Finished! saved image:{self.image_dir}", "info")
                        
                        btn_submit = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.XPATH,"//button[.='Review']")))
                        btn_submit.click()
                        
                        
                        # alert_mess = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.XPATH,f"//*[contains(text(), '{alert}')]")))
                        # alert_url = alert_mess.find_elements(By.XPATH, "//a[.='(2/2) Reviewed link']")
                        # alert_url = alert_url.get_attribute('href')
                        # self.logger.log_message(alert_mess.text, "info")
                        
                        # WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.XPATH,"//a[@class='markdown__link']")))
                        
                        # alert_url = alert_url.get_attribute('href')
                        # (2/2) Reviewed link
                        # alert_url = WebDriverWait(self.driver, self.wait).until(EC.presence_of_element_located((By.XPATH,"//a[.='(2/2) Reviewed link']")))
                        
                        # alert_url = alert_url.get_attribute('href')
                        
                        # alert_url = alert.find_elements(By.XPATH, "//a[.='(2/2) Reviewed link']")
                                                                                
                        # alert_url = alert_url.get_attribute('href')
                        # self.logger.log_message(alert_url, "info")
                        
                        time.sleep(5)
                    except:
                        print("no alert..")
                        time.sleep(5)
                    
                    
                # self.driver.save_screenshot(self.image_dir)  # Saving the screenshot.
                # self.driver.quit()  # Closing the driver instance.
                
                # self.logger.log_message(f"[Take auto click] Finished! saved image:{self.image_dir}", "info")
                
                # return self.image_dir
            
            except Exception as error:
                self.logger.log_message(error, "error")
                self.driver.quit()  # Closing the driver instance.
                return
           
if __name__ == "__main__":  
    
    # KIBANA_DASHBOARD = [{"name": "Web Application Gateway", "id" : "066af8d0-254f-11eb-adf9-436c9a6e2b21", "title": "BGT%20-%20Web%20Application%20Security"},
    #                     {"name": "Brocade Login Summary", "id" : "4f2d8ca0-870a-11eb-8709-b13e589df6d8", "title": "Brocade:%20Login%20Summary"},
    #                     {"name": "Cisco ASA", "id" : "52a56230-53ad-11eb-9ff2-91055408afa2", "title": "CISCO%20ASA"},
    #                     {"name": "DTA SSH Logins", "id" : "48df9c30-5618-11eb-9ff2-91055408afa2", "title": "DTA:%20SSH%20Logins"},
    #                     {"name": "Palo Alto Network", "id" : "0ed27710-53a7-11eb-9ff2-91055408afa2", "title": "Palo%20Alto%20network"},
    #                     {"name": "VulnWhisperer Reporting", "id" : "72051530-448e-11e7-a818-f5f80dfc3590", "title": "VulnWhisperer%20-%20Reporting"},
    #                     {"name": "Watch Guard Dashboard", "id" : "63c5b360-3265-11ed-a09d-7789326d20a2", "title": "Watch%20Guard-Dashboard"},
    #                     {"name": "MalBot Alerts", "id" : "4280b6f0-64b5-11e8-9e8d-39632dc6b766", "title": "malBot:%20Alerts%20(Messages)"}]
    
    
    logger = Logger()
    # chatbot = ChatBot(logger=logger, chatid=-1001610632416, token="6033704274:AAH__3A6NnOc-DuuO-2Z0R8EONNqeykdLQ4")
    # for dashboard in KIBANA_DASHBOARD:
    #     twps = TakeWebPriScr(logger)
    #     capture_img = twps.take_screenshot_kibana(dashboard)
    #     chatbot.send_image(image_path=capture_img, caption="test ErikHorus!")
    
    twps = TakeWebPriScr(logger, image_dir="/core/media/noc/")
    # twps.take_screenshot_virustotal("10.65.253.162")
    # twps.take_screenshot_splunk()
    twps.auto_click()
    
    # twps2 = TakeWebPriScr()
    # twps3 = TakeWebPriScr()
    
    # twps1.take_screenshot_mdr(0, 7)
    # twps1.crop_image((110, 500), (1080,1920))
    # twps.take_screenshot_spidey()
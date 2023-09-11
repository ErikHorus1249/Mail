# from PIL import Image
# import pytesseract

# # Transforming image to string and printing it!
# print(pytesseract.image_to_string(Image.open('test.jpg')))

# from utils.screenshot import TakeWebPriScr
# from utils.log import Logger

# if __name__ == "__main__":
    
#     logger = Logger()
#     twps = TakeWebPriScr(logger=logger, image_dir="/core/media/noc/")
    
#     twps.take_screenshot_virustotal(ip="216.24.213.139")

# import requests

# def get_ip_report(ipaddr: str, api_key: str):
#     try:
#         url = f"https://www.virustotal.com/api/v3/ip_addresses/{ipaddr}"
#         header = f'x-apikey: {api_key}'
#         response = requests.get(url=url, headers=header)
#         return response.json() if response.status_code == 200 else None
#     except Exception as error:
#         print(error)
#         return None
        
# if  __name__ == "__main__":
#     API_KEY = "f25cfc1b646a0d0eb6437fa7a21db4f9cfc4ef8027c97bd3943428acc5bed2d1"
#     URL =  "https://www.virustotal.com/api/v3/ip_addresses/"
    
#     print(get_ip_report(ipaddr="103.186.152.30", api_key=API_KEY))

# IUKIQNS477X52GKOOIY6A4IL4XNDIQQ6

import pyotp

# Replace 'your_secret_key' with your actual secret key (usually a base32-encoded string).
secret_key = 'IUKIQNS477X52GKOOIY6A4IL4XNDIQQ6'
otp = pyotp.TOTP(secret_key)

verification_code = otp.now()
print(f'Current Verification Code: {verification_code}')
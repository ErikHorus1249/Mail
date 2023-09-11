import pyotp

# Replace 'your_secret_key' with your actual secret key (usually a base32-encoded string).

class OTP():
    def __init__(self, secret_key:str) -> None:
        # self.secret_key = secret_key
        self.otp = pyotp.TOTP(secret_key)
        
    def get_otp(self):
        return self.otp.now()
        
        
if __name__ == "__main__":
    newotp = OTP(secret_key="4V45KEXOFWFEOOWBVETQLFPJRZ3E3HPM")
    print(newotp.get_otp())

    
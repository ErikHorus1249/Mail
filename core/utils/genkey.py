from cryptography.fernet import Fernet
import os, ipaddress, random

# get key 
KEY = os.getenv("PASSWORD_KEY")
SUBNETMASK = "10.15.182.0/24"

# encrypt 
def encrypt_password(password: str):
    f = Fernet(bytes(KEY, "utf-8"))
    return (f.encrypt(bytes(password, "ascii"))).decode("utf-8")

# decrypt
def decrypt_password(token: str):
    f = Fernet(bytes(KEY, "utf-8"))
    return (f.decrypt(bytes(token, "utf-8"))).decode("utf-8")

def gen_ip():
    ips = [str(ip) for ip in ipaddress.IPv4Network(SUBNETMASK)]
    return random.choice(ips)

if __name__ == "__main__":
    # token = encrypt_password('chaoban124')
    # print(token)
    # print(decrypt_password("gAAAAABi2YP_PGuTz6usWz2RFN8UY97fycaEr7lKcLfuD9amKGk8VzwJzkyOQfZG5vjqJWvEbTGGmkqd-_0Qyv1zNFxmSfGnvi05kiRzCHIeLJPW57LNd3Q="))
    print(gen_ip())

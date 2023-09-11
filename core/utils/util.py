import re 
import os
import glob
import socket


FINAL_REPORT = os.getenv("FINAL_REPORT")

def clear_old_file(dir: str) -> None:
    try:
        files = glob.glob(f'{dir}*')
        for f in files:
            os.remove(f)
    except Exception as error:
        print(error)
        

ZONE_MAPPING = {
    2: 'PDC',
    3: 'DRC',
    5: 'DRC',
    6: 'PDC',
    7: 'PDC'
}

IPV4_REGEX = re.compile('(10(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}|(172\.(1[6-9]|2[0-9]|3[01]))(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){2})')

def validate_info(text: str):
    return (text.strip()).lower()

def validate_zone(group_id: int) -> str:
    return ZONE_MAPPING.get(group_id, 'UNKNOWN')


def validate_ipv4(raw_text: str) -> str:
    ip = IPV4_REGEX.search(raw_text)
    if ip:
        return ip.group(0)
    else:
        return "127.0.0.1"

def verify_ipv4(ip: str):
    try:
        return socket.inet_aton(ip)
    except:
        return
    
def verify_hash_md5(hash: str):
    try:
        return re.search(r'[0-9a-f]{32}', hash)
    except:
        return
    
def remove_file(file_path: str) -> bool:
    if os.path.isfile(file_path): 
        try:
            os.remove(file_path)
            return not os.path.isfile(file_path)   # Return True if file doesn't exist after deleting it.
        except PermissionError:  # Handle permission errors when trying to remove a file that is currently open/locked.
            print(f"Error: Unable to delete {file_path}. File may be in use.")
            return False
    else:
        print(f"Error: {file_path} file not found")
        return False

# def crop_image(import_img: str, export_img: str, start_point: tuple, end_point: tuple) -> bool:
#     """Crop and save a region of an image.

#     Args:
#         import_img (str): Path to the input image file.
#         export_img (str): Path to the output cropped image file.
#         start_point (tuple): A tuple of two integers representing the starting point (y,x) of the crop.
#         end_point (tuple): A tuple of two integers representing the ending point (h,w) of the crop.

#     Returns:
#         bool: True if the image was successfully cropped and saved, False otherwise.
#     """
#     if not os.path.isfile(import_img):
#         print(f"Error: {import_img} file not found")
#         return False
    
#     img = cv2.imread(import_img)
#     y1, x1 = start_point
#     y2, x2 = end_point
    
#     if y1 >= y2 or x1 >= x2 or y2 > img.shape[0] or x2 > img.shape[1]:
#         print("Error: Invalid cropping points")
#         return False

#     crop = img[y1:y2, x1:x2]
#     cv2.imwrite(export_img, crop)

#     return True

if __name__ == "__main__":
     
    # crop_image(import_img="img/cbr_sample.png", export_img="img/crop_cbr_sample.png", start_point=(110, 500), end_point=(1080,1920))
    
    # crop_image(import_img="img/spd_sample.png", export_img="img/crop_spd_sample.png", start_point=(0,250), end_point=(1080,1920))
    
    clear_old_file()
    
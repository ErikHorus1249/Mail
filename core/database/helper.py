
import os 
import sys
sys.path.insert(0, "/core/database")
# sys.path.insert(0, "/backend/database")
from models import UserModelIN
from models import ShiftModel
from models import ShiftModelIN
from models import AlertModel
from models import ShiftModelIN
from pymongo import MongoClient

sys.path.insert(0, "/core/utils")
from genkey import encrypt_password
from genkey import decrypt_password
from log import Logger
from util import validate_info


MONGODB_URL= os.getenv("MONGO_CONNECTION_STRING")

class Helper():
    def __init__(self, logger: Logger) -> None:
        self.connect = MongoClient(MONGODB_URL).get_database("service-data")
        self.logger = logger

    def get_connection(self):
        return self.connect
    
    def create_user(self, user_data: UserModelIN):
        doc = dict((k, v) for k, v in user_data.dict().items() if v is not None)
        # doc["activated"] = True
        doc['username'] = validate_info(doc['username'])
        doc["password"] = encrypt_password(doc["password"].strip())
        is_exist = self.connect.User.find_one({"username":doc["username"]})
        if is_exist:
            return {"status":False,"detals":"Đã tồn tại tài khoản, vui lòng thử lại."}
        else: 
            try:
                
                inserted_doc = self.connect.User.insert_one(doc) # inser user data 
                self.logger.log_message(f"Chào mừng {doc['teleacc']} đã đến được Vanhalla 🏔! Nâng ly 🍺 chúc mừng nào!", "info")
                return inserted_doc.get('_id')
                
            except:
                return {"status":False,"detals":"Vui lòng liên hệ quản trị viên để được hỗ trợ."}
        
    def create_shift(self, shift_data: dict):
        
        try:
            user_id = self.get_user_by_name(shift_data["username"]).get('_id')
            shift_data['user_id'] = user_id
            
            try:
                return self.connect.Shift.insert_one(shift_data) 
            except:
                print("insert new shift error")
                return
        except:
            pass 
        # is_exist = self.connect.User.find_one({"username":doc["username"]})
        # if is_exist:
        #     return {"status":False,"detals":"Đã tồn tại tài khoản, vui lòng thử lại."}
        # else: 
        #     try:
                
        #         inserted_doc = self.connect.User.insert_one(doc) # inser user data 
        #         self.logger.log_message(f"Chào mừng {doc['teleacc']} đã đến được Vanhalla 🏔! Nâng ly 🍺 chúc mừng nào!", "info")
        #         return inserted_doc.get('_id')
                
        #     except:
        #         return {"status":False,"detals":"Vui lòng liên hệ quản trị viên để được hỗ trợ."}
            
    # def create_schedule(self, shift_data: ShiftModelIN):
    #     doc = dict((k, v) for k, v in shift_data.dict().items() if v is not None)
    #     try:
                
    #         inserted_doc = self.connect.Shift.insert_one(doc) # inser user data 
    #         self.logger.log_message(f"Tạo ca cho {} thành công")
    #         return inserted_doc.get('_id')
            
    #     except:
    #         return {"status":False,"detals":"Vui lòng liên hệ quản trị viên để được hỗ trợ."}
        

    def get_users(self):
        user_list = []
        try:
            users = self.connect.User.find({})
        except Exception as error:
            self.logger.log_message(error, "error")
            self.logger.log_message("Get information about the list of failed users", "error") 
        try:
            for user in users:
                user["password"] = decrypt_password(user["password"])
                user_list.append(UserModelIN.parse_obj(user))
            return user_list
        except TypeError:
            self.logger.log_message("'NoneType' object is not iterable", "error")
            return user_list

    def get_user_by_name(self, username: str):
        try:
            user = self.connect.User.find_one({"username":username})
            user['password'] = decrypt_password(user['password'])
            return user
        except Exception as error:
            self.logger.log_message(error, "error")
            self.logger.log_message("Get information about the list of failed users", "error")        

    def get_user_by_tele(self, tele: str):
        try:
            user = self.connect.User.find_one({"teleacc":tele})
            return user
        except Exception as error:
            self.logger.log_message(error, "error")
            self.logger.log_message("Get information about the list of failed users", "error")    
            return 

# def update_password(username: str, old_password: str, new_password: str):
#     if users := conn.User.find_one({"username": username.strip()}):
#         fetch_data = UserModel.parse_obj(users)
#         if decrypt_password(fetch_data.password) == old_password.strip():
#             return {"status": True, "details": str(conn.User.update_one({"username": username.strip()}, { "$set": {"password": encrypt_password(new_password.strip())}}))}
#         else:
#             return {"status":False, "details":"Mật khẩu cũ của bạn bị sai, vui lòng thử lại."}
#     else: 
#         return  {"status":False, "details":"Người dùng không tồn tại."}
#     return None

# def update_password(username: str, new_password: str):
#     return {"status": True, "details": str(conn.User.update_one({"username": username.strip()}, { "$set": {"password": encrypt_password(new_password.strip())}}))}

        
# def serve_user(mode: int, username: str):
#     try:
#         find_query = { "username": username }
#         if user := conn.User.find_one(find_query):
#             if bool(mode) == True and bool(mode) != user["activated"] :
#                 result = conn.User.update_one(find_query, { "$set": { "activated": True } })
#                 create(f"Cập nhật trạng thái cung cấp dịch vụ đối với người dùng {username}")
#                 # send_message(f"📢Cập nhật trạng thái tiếp tục cung cấp dịch vụ đối với người dùng {user['teleacc']}")
#                 return result
#             elif bool(mode) == False and bool(mode) != user["activated"]:
#                 result = conn.User.update_one(find_query, { "$set": { "activated": False } })
#                 create(f"Cập nhật trạng thái ngừng cung cấp dịch vụ đối với người dùng {username}")
#                 # send_message(f"⚠️Cập nhật trạng thái ngừng cung cấp dịch vụ đối với người dùng {user['teleacc']}")
#                 return result
#             else: 
#                 create(f"Cập nhật thất bại! Trạng thái cập nhật cung cấp dịch vụ đang được áp dụng đối với người dùng {username}")
#                 return None
#         else:
#             return None 
#     except Exception:
#         create_error_log(traceback.format_exc())
#         return None
        


if __name__ == "__main__":
    test = {'email': "hieunm62@fpt.com.vn",
            'username': 'hieunm62', 
            'password': encrypt_password("P!ghieu12345"), 
            'secret': 'GM7HPFZPQ4X64VRCDCTP2JFQEEMHNARA', 
            'teleacc': '@hieungo205', 
            'activated': True}
    
    test_shift = {'start': 1694107191, 
            'duraion': 4, 
            'username': 'anhnt376', 
            }
    
    test_helper = Helper(logger=Logger())
    # print(test_helper.get_connection())
    # result = test_helper.get_user_by_name("anhnt376@fpt.com.vn")
    result = test_helper.connect.User.insert_one(test) 
    # print(test_helper.create_shift(test_shift))
    print(result)
    


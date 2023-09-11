from fastapi import APIRouter
from typing_extensions import Annotated
from fastapi import Form

import sys
sys.path.insert(0, "/core/database")
from helper import Helper
from models import ShiftModelIN
sys.path.insert(0, "/core/utils")
from genkey import encrypt_password
from log import Logger

Shift = APIRouter()

@Shift.post("/Shift", response_description="create shift")

async def create_shift(data: ShiftModelIN):

    logger = Logger()
    helper = Helper(logger)
    insert_id = helper.create_shift(data)
    
    if insert_id:
        return {"status":True,
                "user_id": insert_id,
                }
    else:
        return {"status":False,"detals":"Error"}
    
# @User.delete("/Users", response_description="delete users")
# async def delete_user():
#     if conn.User.delete_many({}): return True
#     else: return False

# @User.get("/Users", response_description="update user's password")
# async def update(username: str, old_pass: str, new_pass: str):
#     return update_password(username, old_pass, new_pass)

# @User.get("/Users", response_description="update user's password")
# async def update(username: str ,new_pass: str):
#     # if get_token(username, new_pass):
#     #     # create(f"Update password successfully! User: {username}")
#     #     await send_message(f"Cập nhật mật khẩu thành công, User: {username}")
#     return update_password(username, new_pass)


@User.get("/_test", response_description="Testing")
def test():
    return  {"data":"ok"}
from ast import Dict
from typing import  Optional
from bson import ObjectId
from pydantic import BaseModel, Field
import uuid
import datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ShiftModel(BaseModel):
    start: int = Field(example="1693628092")
    duration: int = Field(example="4")
    user_id: str
    alert: int

class ShiftModelIN(BaseModel):
    start: int = Field(example="1693628092")
    duration: int = Field(example="4")
    username: str
    
class AlertModel(BaseModel):
    name: str = Field(example="BSR_8101_FPT---IN-SUS-CONN---RECONN---Reconnaissance-activity-in-15m-by-McAfee-NSM")

class UserModel(BaseModel):
    username: str = Field(example="AnhNT123")
    email: str = Field(example="anhnt376@fpt.com")
    password: str = Field(example="********")
    secret: str = Field(example="********")
    teleacc: str = Field(example="@yourteleacc")

class UserModelIN(BaseModel):
    username: str = Field(example="AnhNT123")
    email: str = Field(example="anhnt376@fpt.com")
    password: str = Field(example="********")
    secret: str = Field(example="********")
    teleacc: str = Field(example="@yourteleacc")
    activated: bool
from fastapi import APIRouter
from utils.chatbot import send_message

Chatbot = APIRouter()

@Chatbot.get("/chatbot")
async def send_telegram_message(message: str):
    return send_message(message=message) 
    
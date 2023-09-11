import os
import sys
import asyncio
import traceback
import telebot

sys.path.append("/core/utils/")

from utils.log import Logger

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TOKEN = "6110244769:AAF2ChI_oCdgKDByEJXmWZEvjRHRMoEfZfc"
# JOTUNHEIM = -1001971816433
JOTUNHEIM = -991429495

class ChatBot():
    def __init__(self, logger: Logger, chatid = JOTUNHEIM, token = TOKEN):
        self.chat_id = chatid
        self.bot = telebot.TeleBot(token)
        self.logger = logger
    
    async def send_telegram_message(self, message):
        # await self.bot.send_message(JOTUNHEIM, message, parse_mode= 'Markdown')
        await self.bot.send_message(JOTUNHEIM, message)
    
    async def send_telegram_file(self, file_path):
        with open(file_path, "rb") as file:
            await self.bot.send_document(self.chat_id, file)

    async def send_telegram_image(self, image_path: str, caption: str):
        with open(image_path, "rb") as file:
            await self.bot.send_photo(chat_id=self.chat_id, caption=caption ,photo=open(image_path, 'rb'))
    
    async def send_message(self, message):
        try:
            await self.send_telegram_message(message)
        except Exception as error:
            self.logger.log_message(error, "error")
            self.logger.log_message(traceback.format_exc, "error")
            return "@erikhorus"
        
    async def send_file(self, file_path):
        try:
            await self.send_telegram_file(file_path)
        except Exception as error:
            self.logger.log_message(error, "error")
            self.logger.log_message(traceback.format_exc, "error")
            return "@erikhorus"
    
    async def send_image(self, image_path: str, caption: str = ""):
        try:
            await self.send_telegram_image(image_path, caption)
        except Exception as error:
            pass
            # self.logger.log_message(error, "error")
            # return "@erikhorus"
    
if __name__ == "__main__":
    # asyncio.run(send("mess"))
    chatbot = ChatBot()
    # asyncio.run(chatbot.send_message("Báo cáo BGT ngày"))
    # asyncio.run(chatbot.send_file("/core/media/BGT_Checklist_23_05_2023.zip"))
    # asyncio.run(chatbot.send_file("/core/media/docx_report/BGT_Email_Summary_23_05_2023.docx"))


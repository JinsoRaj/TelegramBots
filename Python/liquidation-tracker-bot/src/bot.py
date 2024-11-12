import os
import asyncio
import bot_keyboards as bk
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

TELEGRAM_CHAT_ID = None
user_id = None

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    global TELEGRAM_CHAT_ID
    TELEGRAM_CHAT_ID = message.chat.id

    await message.answer(f"Hi, {message.from_user.full_name}! I'm a Liquidation Notifier Bot.", reply_markup=bk.main_keyboard())

@dp.message(F.text == "Settings")
async def settings_handler(message: Message):
    await message.answer("Settings menu:", reply_markup=bk.settings_keyboard())

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

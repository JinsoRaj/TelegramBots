import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

TELEGRAM_CHAT_ID = None

def main_keyboard():
    kb = [
        [
            KeyboardButton(text="Binance Liquidations"),
            KeyboardButton(text="BYBIT Liquidations")
        ],
        [
            KeyboardButton(text="Settings"),
            KeyboardButton(text="Stop")
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    global TELEGRAM_CHAT_ID
    TELEGRAM_CHAT_ID = message.chat.id

    await message.answer(f"Hi, {message.from_user.full_name}! I'm a Liquidation Notifier Bot.", reply_markup=main_keyboard())

@dp.message(F.text == "Settings")
async def settings_handler(message: Message):
    kb = [
        [
            KeyboardButton(text="Save Settings")
        ],
        [
            KeyboardButton(text="Liquidation Price"),
            KeyboardButton(text="Crypto Range")
        ],
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer("Settings menu:", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

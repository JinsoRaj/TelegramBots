import os
import asyncio
import bot_keyboards as bk
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

TELEGRAM_CHAT_ID = None
user_id = None

user_liquidation_prices = {}

class LiquidationSettings(StatesGroup):
    waiting_for_liquidation_price = State()

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    global TELEGRAM_CHAT_ID
    TELEGRAM_CHAT_ID = message.chat.id

    await message.answer(f"Hi, {message.from_user.full_name}! I'm a Liquidation Notifier Bot.", reply_markup=bk.main_keyboard())

@dp.message(F.text == "Settings")
async def settings_handler(message: Message):
    await message.answer("Settings menu:", reply_markup=bk.settings_keyboard())

@dp.message(F.text == "Liquidation Price")
async def ask_liquidation_price(message: Message, state: FSMContext):
    global user_id
    user_id = message.chat.id

    if user_id in user_liquidation_prices:
        await message.answer(f"Your current tracking liquidation price is: {user_liquidation_prices[user_id]}")
    else:
        await message.answer("You have not set a liquidation price yet.")
    await message.answer("Please enter the minimum liquidation price you want to track:")
    await state.set_state(LiquidationSettings.waiting_for_liquidation_price)

@dp.message(LiquidationSettings.waiting_for_liquidation_price)
async def set_liquidation_price(message: Message, state: FSMContext):
    try:
        liquidation_price = float(message.text) * 1000
        user_liquidation_prices[message.from_user.id] = liquidation_price
        await message.answer(f"Your liquidation price has been set to {liquidation_price:.2f}")
        await state.clear()
    except ValueError:
        await message.answer("Please enter a valid number for the liquidation price.")

@dp.message(F.text == "Save Settings")
async def save_settings_handler(message: Message, state: FSMContext):
    # user_id = message.from_user.id
    liquidation_price = user_liquidation_prices.get(user_id, "Not set")
    # crypto_range = user_crypto_range.get(user_id, "Not set")

    response_message = (
        "Your settings were updated.\n"
        f"Your current tracking liquidation price is: {liquidation_price}\n"
        f"Your current crypto range: --COMING SOON--"
    )

    await message.answer(response_message, reply_markup=bk.main_keyboard())

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

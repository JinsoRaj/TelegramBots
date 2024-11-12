import os
import asyncio
import bot_keyboards as bk
import methods as m
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

is_binance_connected = False
main_loop = None

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

@dp.message(F.text == "Binance Liquidations")
async def binance_liquidations_handler(message: Message):
    global is_binance_connected
    if not is_binance_connected:
        await message.answer("Binance Liquidations Menu", reply_markup=bk.binance_liquidations_keyboard_not_tracking())
    else:
        await message.answer("Binance Liquidations Menu", reply_markup=bk.binance_liquidations_keyboard_tracking())

@dp.message(F.text == "Back")
async def back_button_handler(message: Message):
    await message.answer("Returning to the main menu", reply_markup=bk.main_keyboard())

@dp.message(F.text == "Start Tracking")
async def start_tracking_handler(message: Message):
    global is_binance_connected
    is_binance_connected = True

    await message.answer("Starting Tracking Liquidations on Binance.", reply_markup=bk.binance_liquidations_keyboard_tracking())

    await asyncio.to_thread(m.connect_binance, main_loop, bot, user_liquidation_prices)

@dp.message(F.text == "Stop Tracking")
async def stop_tracking_handler(message: Message):
    global is_binance_connected
    is_binance_connected = False

    m.disconnect_binance()

    await message.answer("Binance Tracking - Stopped.", reply_markup=bk.binance_liquidations_keyboard_not_tracking())

async def main():
    global main_loop
    main_loop = asyncio.get_running_loop()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

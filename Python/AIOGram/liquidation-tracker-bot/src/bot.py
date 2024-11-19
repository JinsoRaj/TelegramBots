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

# Load environment variables
load_dotenv()

# Telegram bot token from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Global variables to store user information and settings
TELEGRAM_CHAT_ID = None
user_id = None
is_binance_connected = False
main_loop = None

# Trackers for active users and user-specific liquidation prices
active_trackers = set()
user_liquidation_prices = {}

class LiquidationSettings(StatesGroup):
    """State group for handling liquidation settings."""
    waiting_for_liquidation_price = State()

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    """
    Handle the /start command sent by the user.

    Parameters:
        message (Message): The incoming message object from the user.

    Sets the global `TELEGRAM_CHAT_ID` and sends a welcome message.
    """
    global TELEGRAM_CHAT_ID
    TELEGRAM_CHAT_ID = message.chat.id

    await message.answer(
        f"Hi, {message.from_user.full_name}! I'm a Liquidation Notifier Bot.",
        reply_markup=bk.main_keyboard()
    )

@dp.message(F.text == "Settings")
async def settings_handler(message: Message):
    """
    Display the settings menu when the user selects 'Settings'.

    Parameters:
        message (Message): The incoming message object from the user.
    """
    await message.answer("Settings menu:", reply_markup=bk.settings_keyboard())

@dp.message(F.text == "Liquidation Price")
async def ask_liquidation_price(message: Message, state: FSMContext):
    """
    Ask the user for their desired liquidation price to track.

    Parameters:
        message (Message): The incoming message object from the user.
        state (FSMContext): The Finite State Machine context for managing user states.
    """
    global user_id
    user_id = message.chat.id

    if user_id in user_liquidation_prices:
        await message.answer(
            f"Your current tracking liquidation price is: {user_liquidation_prices[user_id]}"
        )
    else:
        await message.answer("You have not set a liquidation price yet.")
    await message.answer("Please enter the minimum liquidation price you want to track:")
    await state.set_state(LiquidationSettings.waiting_for_liquidation_price)

@dp.message(LiquidationSettings.waiting_for_liquidation_price)
async def set_liquidation_price(message: Message, state: FSMContext):
    """
    Set the user's liquidation price based on their input.

    Parameters:
        message (Message): The incoming message object from the user.
        state (FSMContext): The Finite State Machine context for managing user states.

    Converts the user's input to a floating-point value and stores it in `user_liquidation_prices`.
    """
    try:
        liquidation_price = float(message.text) * 1000
        user_liquidation_prices[message.from_user.id] = liquidation_price
        await message.answer(f"Your liquidation price has been set to {liquidation_price:.2f}")
        await state.clear()
    except ValueError:
        await message.answer("Please enter a valid number for the liquidation price.")

@dp.message(F.text == "Save Settings")
async def save_settings_handler(message: Message, state: FSMContext):
    """
    Save the user's current settings and display a confirmation message.

    Parameters:
        message (Message): The incoming message object from the user.
        state (FSMContext): The Finite State Machine context for managing user states.
    """
    liquidation_price = user_liquidation_prices.get(user_id, "Not set")

    response_message = (
        "Your settings were updated.\n"
        f"Your current tracking liquidation price is: {liquidation_price}\n"
        f"Your current crypto range: --COMING SOON--"
    )

    await message.answer(response_message, reply_markup=bk.main_keyboard())

@dp.message(F.text == "Binance Liquidations")
async def binance_liquidations_handler(message: Message):
    """
    Display the Binance liquidations menu.

    Parameters:
        message (Message): The incoming message object from the user.
    """
    user_id = message.chat.id
    if user_id not in active_trackers:
        await message.answer(
            "Binance Liquidations Menu",
            reply_markup=bk.binance_liquidations_keyboard_not_tracking()
        )
    else:
        await message.answer(
            "Binance Liquidations Menu",
            reply_markup=bk.binance_liquidations_keyboard_tracking()
        )

@dp.message(F.text == "BYBIT Liquidations")
async def binance_liquidations_handler(message: Message):
    """
    Display a placeholder message for BYBIT liquidations.

    Parameters:
        message (Message): The incoming message object from the user.
    """
    await message.answer("--COMING SOON--", reply_markup=bk.main_keyboard())

@dp.message(F.text == "Back")
async def back_button_handler(message: Message):
    """
    Return the user to the main menu.

    Parameters:
        message (Message): The incoming message object from the user.
    """
    await message.answer("Returning to the main menu", reply_markup=bk.main_keyboard())

@dp.message(F.text == "Start Tracking")
async def start_tracking_handler(message: Message):
    """
    Start tracking Binance liquidations for the user.

    Parameters:
        message (Message): The incoming message object from the user.

    Adds the user's chat ID to `active_trackers` and sends a confirmation message.
    """
    global active_trackers

    active_trackers.add(message.chat.id)
    print(f"New active tracker - {active_trackers}")

    await message.answer(
        "Starting Tracking Liquidations on Binance. You will receive notifications.",
        reply_markup=bk.binance_liquidations_keyboard_tracking()
    )

@dp.message(F.text == "Stop Tracking")
async def stop_tracking_handler(message: Message):
    """
    Stop tracking Binance liquidations for the user.

    Parameters:
        message (Message): The incoming message object from the user.

    Removes the user's chat ID from `active_trackers` and sends a confirmation message.
    """
    global active_trackers

    active_trackers.discard(message.chat.id)
    print(f"Active tracker {active_trackers} - disconnected.")
    await message.answer(
        "Binance Tracking Stopped. You will no longer receive notifications.",
        reply_markup=bk.binance_liquidations_keyboard_not_tracking()
    )

async def main():
    """
    Main entry point for the bot.

    Starts the Binance WebSocket connection and begins polling for messages.
    """
    global main_loop
    main_loop = asyncio.get_running_loop()

    await m.connect_binance(main_loop, bot, user_liquidation_prices, active_trackers)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

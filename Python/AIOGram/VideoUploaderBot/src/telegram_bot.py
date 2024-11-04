import asyncio
import logging
import sys
import os

from user_data_handler import DataHandler
from chrome_profiles import DolphinProfiles
from api_handler import ApiHandler
from aiogram import Bot, Dispatcher, html, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()

form_router = Router()


class Form(StatesGroup):
    api_key = State()
    social_platform = State()
    social_platform_settings = State()
    social_platform_schedule = State()


def platform_list_keyboard():
    kb = [
        [KeyboardButton(text="YouTube")],
        [KeyboardButton(text="Change API key")]
    ]
    return kb


def youtube_keyboard():
    kb = [
        [KeyboardButton(text="Set up a schedule")],
        [KeyboardButton(text="Enable Youtube Uploader")],
        [KeyboardButton(text="Disable Youtube Uploader")],
        [KeyboardButton(text="Back to Menu")]
    ]
    return kb


def schedule_keyboard():
    kb = [
        [KeyboardButton(text="Add daily schedule")],
        [KeyboardButton(text="Back to Youtube Menu")]
    ]
    return kb


def back_to_schedule_menu_keyboard():
    kb = [
        [KeyboardButton(text="Back to Schedule Menu")]
    ]
    return kb


@form_router.message(CommandStart())
async def process_youtube_platform(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.api_key)
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! Send your DolphinAnty API key.",
                         reply_markup=ReplyKeyboardRemove())


@form_router.message(Form.api_key)
async def process_api_key(message: Message, state: FSMContext) -> None:
    api_key = message.text.strip()
    user_id = message.from_user.id

    if await api_handler.api_saver(user_id, api_key):
        await message.answer("API key was added successfully!", reply_markup=ReplyKeyboardRemove())
        await state.update_data(api_key=api_key)
        await state.set_state(Form.social_platform)
        keyboard = ReplyKeyboardMarkup(keyboard=platform_list_keyboard(), resize_keyboard=True)
        await message.answer("Welcome to the Main Menu"
                             , reply_markup=keyboard)
    else:
        await message.answer("Oops! The API key is not valid. Please provide a new one.",
                             reply_markup=ReplyKeyboardRemove())


@form_router.message(Form.social_platform, F.text.casefold() == "youtube")
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.social_platform)
    keyboard = ReplyKeyboardMarkup(keyboard=youtube_keyboard(), resize_keyboard=True)
    await message.answer("Welcome to the Youtube Settings"
                         , reply_markup=keyboard)


@form_router.message(Form.social_platform_settings, F.text.casefold() == "back to youtube menu")
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.social_platform)
    keyboard = ReplyKeyboardMarkup(keyboard=youtube_keyboard(), resize_keyboard=True)
    await message.answer("Welcome back to the Youtube Settings"
                         , reply_markup=keyboard)


@form_router.message(Form.social_platform, F.text.casefold() == "change api key")
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.api_key)
    await state.update_data(api_key=None)
    await message.answer(f"Send your DolphinAnty API key", reply_markup=ReplyKeyboardRemove())


@form_router.message(Form.social_platform, F.text.casefold() == "back to menu")
async def command_start(message: Message) -> None:
    keyboard = ReplyKeyboardMarkup(keyboard=platform_list_keyboard(), resize_keyboard=True)
    await message.answer(f"Welcome to the Main Menu", reply_markup=keyboard)


@form_router.message(Form.social_platform_settings, F.text.casefold() == "back to schedule menu")
async def command_start(message: Message, state: FSMContext) -> None:
    keyboard = ReplyKeyboardMarkup(keyboard=schedule_keyboard(), resize_keyboard=True)
    await message.answer("Welcome back to Schedule Menu"
                         , reply_markup=keyboard)


@form_router.message(Form.social_platform, F.text.casefold() == "set up a schedule")
async def set_up_a_schedule(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.social_platform_settings)
    keyboard = ReplyKeyboardMarkup(keyboard=schedule_keyboard(), resize_keyboard=True)
    await message.answer(f"Choose one option.", reply_markup=keyboard)


@form_router.message(Form.social_platform_settings, F.text.casefold() == "add daily schedule")
async def set_up_a_schedule(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.social_platform_schedule)
    await state.update_data(social_platform_schedule="daily")
    await message.answer(f"Send times in format: HH:MM:SS, HH:MM:SS, ...", reply_markup=ReplyKeyboardRemove())


@form_router.message(Form.social_platform_settings, F.text.casefold() == "enable youtube uploader")
async def enable_bot(message: Message):
    await dolphin_profiles.start_tasks()
    await message.answer("Bot is now enabled and background tasks are running.")


@form_router.message(Form.social_platform_settings, F.text.casefold() == "disable youtube uploader")
async def disable_bot(message: Message):
    await dolphin_profiles.stop_tasks()
    await message.answer("Bot is now disabled and background tasks have been stopped.")


@form_router.message(Form.social_platform_schedule)
async def process_schedule(message: Message, state: FSMContext) -> None:
    date_time = message.text.strip()
    user_id = message.from_user.id
    state_data = await state.get_data()

    schedule = state_data.get("social_platform_schedule", "<something unexpected>")

    result = True
    datetime_list = [component.strip() for component in date_time.split(',')]

    if schedule == "daily":
        if not await data_handler.setup_user_schedule(user_id=user_id, daily_upload_times=datetime_list):
            result = False
            await message.answer("Oops! The schedule has not valid format. Please provide a new one.",
                                 reply_markup=ReplyKeyboardRemove())
    if result is True:
        await message.answer("Schedule was successfully added!", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.social_platform_settings)
        keyboard = ReplyKeyboardMarkup(keyboard=schedule_keyboard(), resize_keyboard=True)
        await message.answer(f"Choose one option.", reply_markup=keyboard)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_router(form_router)

    await data_handler.table_creation()
    await data_handler.daily_upload_times_table_creation()
    await data_handler.upload_log_table_creation()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    data_handler = DataHandler()
    api_handler = ApiHandler()
    dolphin_profiles = DolphinProfiles()

    asyncio.run(main())

""" loads the data that will be used globally in the bot """

import os
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from lib.spotify import Spotify

load_dotenv('.env')

# disable the aiogram logger
logging.getLogger('aiogram').setLevel(logging.CRITICAL)

bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

spotify = Spotify(os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET'))
from InternFreak import bot, loop
from pyrogram import Client, filters
from pyrogram.types import *
from pyrogram.errors import FloodWait
from ..Database.Deta import *
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(1)

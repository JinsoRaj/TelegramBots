#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Made by @Jigarvarma2005

# Edit anything at your own risk

from PIL import Image
import os
from telegraph import upload_file
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

LIMIT = 5242880*2

jvbot = Client(
    "Telegraph bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START_TEXT = """
Hello {}, I' am Telegraph Uploader bot.

- I will download the given media and upload it to telegraph server
- Maxx limit 5mb of a file 

Made by @Jigarvarma2005
"""

@jvbot.on_message(filters.command(["start"]) & filters.private)
async def start_t(bot, message):
    await message.reply_text(
        text=START_TEXT.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Updates Channel', url='https://t.me/UniversalBotsUpdate'), InlineKeyboardButton('Support Group', url='https://t.me/UniversalBotsSupport')]])
    )


@jvbot.on_message(filters.media & filters.sticker)
async def telegraph(bot, message):
    DOWNLOAD_DIRECTORY = "./Downloads"
    editable = await message.reply_text("Downloading to my server")
    if not ((message.photo and message.photo.file_size <= LIMIT)
            or (message.animation and message.animation.file_size <= LIMIT)
            or (message.video and message.video.file_size <= LIMIT)
            or (message.sticker)
            or (message.document
                and message.document.file_name.endswith(
                    ('.jpg', '.jpeg', '.png', '.gif', '.mp4'))
                and message.document.file_size <= LIMIT)):
        await editable.edit("This media is not supported!......")
        return
    await editable.edit("Now I'am Uploading to telegra.ph server ...")
    down_loc = await bot.download_media(
        message=message.reply_to_message,
        file_name=DOWNLOAD_DIRECTORY
    )
    if message.sticker:
        img = Image.open(down_loc).convert('RGB')
        img.save(f'{DOWNLOAD_DIRECTORY}/jigarvarma2005-{message.from_user.id}.png', 'png')
        os.remove(down_loc)
        down_loc = f'{DOWNLOAD_DIRECTORY}/jigarvarma2005-{message.from_user.id}.png'
    await editable.edit("`Uploading to telegraph plox wait....`")
    try:
        response = upload_file(down_loc)
    except Exception as t_e:
        await editable.edit(t_e)
    else:
        await editable.edit(text=f"Successfully Uploaded to telegraph \n**[Telegra.ph Link!](https://telegra.ph{response[0]})**",
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Open Link", url=f"https://telegra.ph{response[0]}"), InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}")]]),
                            disable_web_page_preview=False
                            )
    finally:
        os.remove(down_loc)

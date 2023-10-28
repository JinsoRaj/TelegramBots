# (c) HYBRID
import os
import asyncio
import aiohttp
import logging
import base64

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ReplyKeyboardMarkup
from config import API_ID, API_HASH, BOT_TOKEN, OWNER, BIN_CHANNEL, OCR_SPACE_API_KEY, UPDATES_CHANNEL
from trans import START_MESSAGE, HELP_MESSAGE, ABOUT_MESSAGE, LANGUAGE_MAPPING
from db import usersdb, is_served_user, add_served_user, user_ocr_count, add_user_ocr, update_user_language, user_lang, get_served_users, get_total_use_count, get_total_users_count

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = Client(
    "ocrbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("users") & filters.user(OWNER))
async def get_users_ids(_, message: Message):
    reply_message = await message.reply_text("`Checking users count...`")

    served_users = await get_served_users()
    
    user_ids = [str(chat["user_id"]) for chat in served_users]
    
    users_file = "\n".join(user_ids)
    
    await reply_message.edit_text(f"`{len(user_ids)} users found on db`")
    await reply_message.edit_text(f"`{len(user_ids)} users found on db` \n**Creating userlist file...**")
    
    file_message = await message.reply_text("`Creating userlist file...`")
    with open("user_ids.txt", "w") as file:
        for i, user_id in enumerate(user_ids):
            file.write(user_id + "\n")
            if (i + 1) % 1000 == 0:
                await file_message.edit_text(f"`Creating userlist file... {i+1}/{len(user_ids)}`")
    
    await file_message.edit_text("`Userlist file created.`")
    
    await app.send_document(chat_id=message.chat.id, document="user_ids.txt", file_name="user_ids.txt")
    
    os.remove("user_ids.txt")

@app.on_message(filters.command("start"))
async def start(_, message: Message):
    user_id = int(message.from_user.id)
    ckeck_user = await is_served_user(user_id)
    if not ckeck_user:
        await add_served_user(user_id, message)
        await app.send_message(
            BIN_CHANNEL,
            f"**New User Joined:** \n\nNew User {message.from_user.mention} (`{message.from_user.id}`) started your bot!"
        )
    

    if UPDATES_CHANNEL:
        try:
            user = await app.get_chat_member(UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await app.send_message(
                    chat_id=message.chat.id,
                    text="Sorry, You are banned from using me. Try contacting support @Hybrid_Chat",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
             await app.send_message(
                chat_id=message.chat.id,
                text="<i>Join Updates Channel to use me 🔐</i>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                
            )
             return
        except Exception:
            await app.send_message(
                chat_id=message.chat.id,
                text="<i>Something went wrong</i> <b> <a href='https://t.me/hybrid_chat'>CLICK HERE FOR SUPPORT </a></b>",
                disable_web_page_preview=True)
            return


    keyboard = [
        [
            InlineKeyboardButton("❔ Help", callback_data="help"),
            InlineKeyboardButton("❕ About", callback_data="about"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    count = await user_ocr_count(user_id)
    await message.reply_text(
        START_MESSAGE.format(message.from_user.mention, count),
        reply_markup=reply_markup
    )

@app.on_message(filters.command("help"))
async def start(_, message: Message):
    user_id = int(message.from_user.id)
    ckeck_user = await is_served_user(user_id)
    if not ckeck_user:
        await add_served_user(user_id, message)
        await app.send_message(
            BIN_CHANNEL,
            f"**New User Joined:** \n\nNew User {message.from_user.mention} (`{message.from_user.id}`) started your bot!"
        )


    if UPDATES_CHANNEL:
        try:
            user = await app.get_chat_member(UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await app.send_message(
                    chat_id=message.chat.id,
                    text="Sorry, You are banned from using me. Try contacting support @Hybrid_Chat",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
             await app.send_message(
                chat_id=message.chat.id,
                text="<i>Join Updates Channel to use me 🔐</i>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                
            )
             return
        except Exception:
            await app.send_message(
                chat_id=message.chat.id,
                text="<i>Something went wrong</i> <b> <a href='https://t.me/hybrid_chat'>CLICK HERE FOR SUPPORT </a></b>",
                disable_web_page_preview=True)
            return


    help_buttons = [
            InlineKeyboardButton("🔙 Back", callback_data="back"),
            InlineKeyboardButton("❕ About", callback_data="about"),
        ]
    await message.reply_text(
        HELP_MESSAGE, reply_markup=InlineKeyboardMarkup([help_buttons])
    )
    
@app.on_message(filters.command("about"))
async def start(_, message: Message):
    user_id = int(message.from_user.id)
    ckeck_user = await is_served_user(user_id)
    if not ckeck_user:
        await add_served_user(user_id, message)
        await app.send_message(
            BIN_CHANNEL,
            f"**New User Joined:** \n\nNew User {message.from_user.mention} (`{message.from_user.id}`) started your bot!"
        )
       

    if UPDATES_CHANNEL:
        try:
            user = await app.get_chat_member(UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await app.send_message(
                    chat_id=message.chat.id,
                    text="Sorry, You are banned from using me. Try contacting support @Hybrid_Chat",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
             await app.send_message(
                chat_id=message.chat.id,
                text="<i>Join Updates Channel to use me 🔐</i>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                
            )
             return
        except Exception:
            await app.send_message(
                chat_id=message.chat.id,
                text="<i>Something went wrong</i> <b> <a href='https://t.me/hybrid_chat'>CLICK HERE FOR SUPPORT </a></b>",
                disable_web_page_preview=True)
            return

    total_use_count = await get_total_use_count()
    users_count = await get_total_users_count()
    about_buttons = [
            InlineKeyboardButton("🔙 Back", callback_data="back"),
            InlineKeyboardButton("❔ Help", callback_data="help"),
        ]
    await message.reply_text(
        ABOUT_MESSAGE.format(users_count, total_use_count),
        reply_markup=InlineKeyboardMarkup([about_buttons])
    )

@app.on_callback_query()
async def callback_handlers(_, callback_query):
    data = callback_query.data
    if data == "help":
        help_buttons = [
            InlineKeyboardButton("🔙 Back", callback_data="back"),
            InlineKeyboardButton("❕ About", callback_data="about"),
        ]
        await callback_query.message.edit(
            HELP_MESSAGE, reply_markup=InlineKeyboardMarkup([help_buttons])
        )
    elif data == "about":
        total_use_count = await get_total_use_count()
        users_count = await get_total_users_count()
        about_buttons = [
            InlineKeyboardButton("🔙 Back", callback_data="back"),
            InlineKeyboardButton("❔ Help", callback_data="help"),
        ]
        await callback_query.message.edit(
            ABOUT_MESSAGE.format(users_count, total_use_count),
            reply_markup=InlineKeyboardMarkup([about_buttons])
        )
    elif data == "back":
        keyboard = [
            [
                InlineKeyboardButton("❔ Help", callback_data="help"),
                InlineKeyboardButton("❕ About", callback_data="about"),
            ]
        ]
        user_id = callback_query.from_user.id
        count = await user_ocr_count(user_id)
        await callback_query.message.edit(
            START_MESSAGE.format(callback_query.from_user.mention, count),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


@app.on_message(filters.private & filters.command("lang", prefixes="/"))
async def set_language(_, message: Message):

    if UPDATES_CHANNEL:
        try:
            user = await app.get_chat_member(UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await app.send_message(
                    chat_id=message.chat.id,
                    text="Sorry, You are banned from using me. Try contacting support @Hybrid_Chat",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
             await app.send_message(
                chat_id=message.chat.id,
                text="<i>Join Updates Channel to use me 🔐</i>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                
            )
             return
        except Exception:
            await app.send_message(
                chat_id=message.chat.id,
                text="<i>Something went wrong</i> <b> <a href='https://t.me/hybrid_chat'>CLICK HERE FOR SUPPORT </a></b>",
                disable_web_page_preview=True)
            return


    if len(message.command) == 1:
        languages_list = "\n".join([f"{lang}: {code}" for lang, code in LANGUAGE_MAPPING.items()])
        await message.reply_text("Please specify a language code.\n\nAvailable languages:\n\n" + languages_list)
        return

    language_code = message.command[1]
    if language_code not in LANGUAGE_MAPPING.values():
        if language_code not in LANGUAGE_MAPPING:
            await message.reply_text("Invalid language code or name. Please use the correct language code or name.")
            return
        else:
            language_code = LANGUAGE_MAPPING[language_code]
            language_name = next((lang for lang, code in LANGUAGE_MAPPING.items() if code == language_code), None)

    user_id = int(message.from_user.id)
    await update_user_language(user_id, language_code)
    await message.reply_text(f"Your preferred language has been set to **{language_name}**")


@app.on_message(filters.private & (filters.document | filters.photo))
async def ocr_command(_, message: Message):
    progress_message = await message.reply_text("`Processing image...` 🛠️")
    user_id = int(message.from_user.id)
    check_user = await is_served_user(user_id)

    if not check_user:
        await add_served_user(user_id, message)
        await app.send_message(
            BIN_CHANNEL,
            f"**New User Joined:** \n\nNew User {message.from_user.mention} (`{message.from_user.id}`) started your bot!"
        )


    if UPDATES_CHANNEL:
        try:
            user = await app.get_chat_member(UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await progress_message.edit_text(
                    #chat_id=message.chat.id,
                    text="Sorry, You are banned from using me. Try contacting support @Hybrid_Chat",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
             await progress_message.edit_text(
                #chat_id=message.chat.id,
                text="<i>Join Updates Channel to use me 🔐</i>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                
            )
             return
        except Exception:
            await progress_message.edit_text(
                #chat_id=message.chat.id,
                text="<i>Something went wrong</i> <b> <a href='https://t.me/hybrid_chat'>CLICK HERE FOR SUPPORT </a></b>",
                disable_web_page_preview=True)
            return


    user_language = await user_lang(user_id)

    if message.document:
        if message.document.mime_type not in ["image/png", "image/jpeg"]:
            await progress_message.edit_text("Please send an image or document in PNG or JPEG format.")
            return
        file_id = message.document.file_id
        file_path = await app.download_media(message.document)
    elif message.photo:
        file_id = message.photo.file_id
        file_path = await app.download_media(message.photo)
    else:
        await progress_message.edit_text("Please send an image or document in PNG or JPEG format.")
        return

    with open(file_path, "rb") as file:
        file_content = file.read()

    api_url = "https://api.ocr.space/parse/image"
    headers = {"apikey": OCR_SPACE_API_KEY}
    data = {
        "isOverlayRequired": False,
        "isCreateSearchablePdf": False,
        "isSearchablePdfHideTextLayer": False,
        "language": user_language
    }

    encoded_file_content = base64.b64encode(file_content).decode("utf-8")
    data["base64Image"] = f"data:image/png;base64,{encoded_file_content}"
    
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, data=data) as response:
            if response.status == 200:
                await progress_message.edit_text("`OCR processing...`")
                ocr_result = (await response.json()).get("ParsedResults", [])
                
                if ocr_result:
                    extracted_text = ocr_result[0].get("ParsedText", "")
                    await progress_message.edit_text(f"Extracted Text:\n\n`{extracted_text}` \n\n💬 **Support chat:** @Hybrid_Chat")
                    await add_user_ocr(user_id, message)
                else:
                    await progress_message.edit_text("No text found in the image.")
            else:
                error_message = (await response.json()).get("ErrorMessage", "Unknown error")
                await progress_message.edit_text(f"OCR failed: {error_message}")

    os.remove(file_path)


@app.on_message(filters.command("broadcast") & filters.user(OWNER))
async def broadcast_message(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Please use `/broadcast` as reply to the message you want to broadcast."
        )
    sleep_time = 0.1
    sent = 0
    error = 0
    schats = await get_served_users()
    chats = [int(chat["user_id"]) for chat in schats]
    text = message.reply_to_message.text.markdown
    reply_message = message.reply_to_message

    # Check if the replied message contains any buttons
    reply_markup = None
    if reply_message.reply_markup:
        reply_markup = InlineKeyboardMarkup(reply_message.reply_markup.inline_keyboard)

    m = await message.reply_text(
        f"Broadcast in progress, will take {len(chats) * sleep_time} seconds."
    )

    for i in chats:
        try:
            # Send the entire replied message with the same buttons if any
            await app.send_message(
                i,
                text=text,
                reply_markup=reply_markup,
            )
            await asyncio.sleep(sleep_time)
            sent += 1
        except FloodWait as e:
            await asyncio.sleep(int(e.value))
        except Exception as e:
            log.error(f"Broadcast error: {e}")
            error += 1
            pass
    await m.edit(f"**Broadcasted Message to {sent} Users.**\n\nError: {error}")


log.info("Initializing Bot client")
app.run()
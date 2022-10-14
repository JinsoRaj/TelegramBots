from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
from wserver import keep_alive
from modules.ouo import ouo_bypass
logging.basicConfig(level=logging.INFO)

for log_name, log_obj in logging.Logger.manager.loggerDict.items():
    if log_name != 'pyrogram':
        log_obj.disabled = True

LOGGER = logging.getLogger(__name__)

API_ID = ' Your telegram API_ID'
API_HASH = 'Your telegram API_HASH'
BOT_TOKEN = 'Your telegram BOT_TOKEN'

bot = Client('shortlinkurlbypasserbot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    LOGGER.info(f"{message.chat.first_name} Just Started me")
    await message.reply(f'''**Hi {message.chat.first_name}!**\n'''
                        '''I'm Ouo Link Bypasser Bot.\n
        <b>Send Me Ouo Shortened Url And I Will Give You Direct Link</b>
        
        <b>╭──「⭕️ **Supported Sites** ⭕️」</b>
        <b>├1️⃣  Ouo.io</b>
        <b>╰──「🚀 BOT BY @RoarCyber 🚀」</b>
       ''')
#Ouo Open
@bot.on_message(filters.regex(r'\bhttps?://.*ouo\S+') & filters.private)
async def ouo_link_handler(bot, message):
    url = message.matches[0].group(0)
    try:
     await message.reply(f'Pʟᴇᴀsᴇ Wᴀɪᴛ Bʏᴘᴀssɪɴɢ Yᴏᴜʀ Uʀʟ')   
     bypassed = await ouo_bypass(url)
     BUTTONS = [
       [
         InlineKeyboardButton('Oʀɪɢɪɴᴀʟ Uʀʟ', url = url),
         InlineKeyboardButton('Bʏᴘᴀssᴇᴅ Uʀʟ', url = bypassed)
       ]
     ]
     reply_markup=InlineKeyboardMarkup(BUTTONS)
     await message.reply(
       (f'❤️{message.chat.first_name} Yᴏᴜʀ Lɪɴᴋ Hᴀs Bᴇᴇɴ Bʏᴘᴀssᴇᴅ \n 👇 Cʜᴇᴄᴋ Tʜᴇ Bᴜᴛᴛᴏɴs Bᴇʟᴏᴡ\n Powered ʙʏ <b>@RoarCyber</b>'),
       reply_markup=reply_markup
     )
    except Exception as e:
        LOGGER.error(e)
        await message.reply(f'Eɴᴄᴏᴜɴᴛᴇʀᴇᴅ ᴀ ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴏᴡɴᴇʀs', quote=True) 

#OUO CLOSED

# ==============================================
LOGGER.info('I AM ALIVE')
keep_alive()
bot.run()

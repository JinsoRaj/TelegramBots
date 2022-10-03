"""
MRVISHAL2K2
Simple Url uploader
"""
import os, asyncio, logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# pyrogram logging
import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.parser").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.session").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

import pySmartDL
from pySmartDL import SmartDL  

from pyrogram import Client, filters
from .config import *

Bot = Client(
    name="DownloadRobot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    sleep_threshold=15,
)


async def link_download(url, download_path, message): 
  await message.edit_text(text="Starting Download...") 
  obj = SmartDL(url, download_path, progress_bar=False) 
  obj.start(blocking=False)
  while not obj.isFinished():
      progress = str(obj.get_progress()*100).split(".")[0]
      downloaded = obj.get_dl_size(human=True)
      total = obj.get_final_filesize(human=True)
      speed = obj.get_speed(human=True)
      eta = obj.get_eta(human=True)
      mess_age="""Downloading...
Progress: {b}%
Downloaded 📥: {d} 
Total Size : {e} 
Speed 🚀 : {f} 
Time Left ⏳: {g}
""".format(b=progress, 
             d=downloaded, e=total, f=speed, g=eta)
      try:
         await message.edit(text=mess_age)
      except:
          pass
      await asyncio.sleep(3)
  if obj.isSuccessful():
    down_path = str(obj.get_dest()) 
    return down_path
  else:   
      return None
    
    
@Bot.on_message(filters.command("start"))
async def start_(c, m):
    await m.reply("Running\n send directlinks to see magic")
    
@Bot.on_message(filters.private & filters.regex(pattern=".*http.*"))
async def down_(c, m):
  msg = await m.reply("Processing.. ", True)
  url = m.text.strip().rstrip()
  downdir = f"./downloads/{m.from_user.id}/{msg.id}/"
  os.makedirs(downdir, exist_ok=True)
  output = await link_download(url, downdir, msg)
  if (output == downdir) or (output == None):
    return await msg.edit("Failed to download")
  # else basic doc way upload no progress
  await msg.edit("Uploading please wait")
  await m.reply_document(document=file, quote=True)
  
  await msg.edit("Uploaded") 
  
  
if __name___ == '__main__'
  logger.info("Starting Bot")
  Bot.run()
  
    

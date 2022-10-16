from pyrogram import Client, filters
from identifiers import *
from scrape import get_link,get_trib

Bot = Client(
	name="antbot",
	api_id=123456,
	api_hash="",
	bot_token="",
	sleep_threshold=15,
)


	
@Bot.on_message(filters.command("start"))
async def start_(c, m):
	await m.reply("send a mkvking link")
	
@Bot.on_message(filters.private & filters.regex(pattern=".*http.*"))
async def down_(c, m):
  msg = await m.reply("Processing.. ", True)
  url = m.text.strip().rstrip()
  links = get_trib(url,MG)  
  for i in links:
   r = get_link(i)
   await msg.reply(r) 
  

if __name__ == '__main__':
  Bot.run()
  
	

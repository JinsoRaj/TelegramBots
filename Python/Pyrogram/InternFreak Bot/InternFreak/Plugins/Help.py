from .__init__ import *

MSG = """
<b>🗒️ Available Commands</b>

<b>● /start - To Start the Bot</b>
<b>● /help - To get this message</b>
<b>● /about - To get info about meh and this Bot</b>
<b>● /subscribe - To subscribe to feeds Bot will send feeds in PM</b>
<b>● /unsubscribe - To unubscribe to feeds</b>

┈┈┈••✿ @InternFreakPosts ✿••┈┈┈
"""


@bot.on_message(filters.command(['help', 'help@internfreakbot']))
async def about(app, message):
    await app.send_message(message.chat.id, MSG)

from .__init__ import *


@bot.on_message(filters.command(['start', 'start@internfreakbot']) & filters.private)
def command3(app, message):
    app.send_message(message.chat.id, "<code>I am Alive :)</code>")

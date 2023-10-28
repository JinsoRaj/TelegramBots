# (c) HYBRID
import os

START_MESSAGE = """
Hello {} 👋

i'm an OCR (Optical Character recognition) Bot.
I can help you to Extract text from images.
Check **❔ Help** menu for more details

📈 Your OCR usage: `{}`

💬 Support: @Hybrid_Chat
"""

HELP_MESSAGE = """
**How to use the bot** ❔

> __Just send the image containing text as an image or as document__ 
> __Use /lang command to see the supported languages and its codes__
    Usage: `/lang language-code`
    Eg: `/lang eng`

❕ Note: `Document must be in PNG/JPEG Format`
                                          
💬 Support: @Hybrid_Chat
"""

ABOUT_MESSAGE = """
**About @TheOCRoBot**

 🤖 Version : 0.3.1
 📝 Language: Python
 📚 Library : Pyrogram 2.0
 ☁️ Server  : VPS
 👤 Creator : @Hybrid_Vamp
 💬 Support : @Hybrid_Chat
 📢 Updates : @Hybrid_Bots

 👥 Total users     : {} 
 📈 Total OCR count : {}
 """

LANGUAGE_MAPPING = {
    "Arabic": "ara",
    "Bulgarian": "bul",
    "Chinese (Simplified)": "chs",
    "Chinese (Traditional)": "cht",
    "Croatian": "hrv",
    "Czech": "cze",
    "Danish": "dan",
    "Dutch": "dut",
    "English": "eng",
    "Finnish": "fin",
    "French": "fre",
    "German": "ger",
    "Greek": "gre",
    "Hungarian": "hun",
    "Korean": "kor",
    "Italian": "ita",
    "Japanese": "jpn",
    "Polish": "pol",
    "Portuguese": "por",
    "Russian": "rus",
    "Slovenian": "slv",
    "Spanish": "spa",
    "Swedish": "swe",
    "Turkish": "tur",
    "Hindi": "hin",
    "Kannada": "kan",
    "Persian (Farsi)": "per",
    "Telugu": "tel",
    "Tamil": "tam",
    "Thai": "tai",
    "Vietnamese": "vie"
}
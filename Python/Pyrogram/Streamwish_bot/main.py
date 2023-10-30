#####################################
##                                 ##
##      Work By CyberNobie         ##
##  https://github.com/cybernobie  ##
##                                 ##
#####################################
import requests
import os
from pyrogram import Client, filters
import time

BASE_URL = "https://api.streamwish.com/api"  # StreamWish API base URL
API_KEY = ""  # Replace with your StreamWish API key/token
# Define headers with API key
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# Your Telegram API ID
API_ID = ''
# Your Telegram API HASH
API_HASH = ''
# Your Telegram BOT token
BOT_TOKEN = ''
# List of approved user IDs
approved_users = [1010583341] # [ ID1 , ID2 , ..]
# Create the Pyrogram client
app = Client("streamflix_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Account Information
def get_account_info():
    response = requests.get(f"{BASE_URL}/account/info?key={API_KEY}", headers=headers)
    data_ac_info=response.json()
    return data_ac_info

   

@app.on_message(filters.command("start"))
def start(bot, message):
    bot.send_message(message.chat.id, 'Welcome to the Streamflix Bot! Use /help for more')

@app.on_message(filters.command("help"))
def help(bot,message):
    bot.send_message(message.chat.id, 'User Commands\n/accountinfo - Account Information\n/accountstats -  Account Stats \n\nBot By @RoarCyber')

# account info open  
@app.on_message(filters.command("accountinfo"))
def accountinfo(bot,message):
    if message.from_user.id not in approved_users:
        bot.send_message(message.chat.id, "You are not an approved user.")
        return
    else:
        clear_screen()
        account_info = get_account_info()
        Storage_KB = account_info["result"]["storage_used"]
        storage_info = Storage_KB / 1000000
        bot.send_message(message.chat.id, f'<b>Showing Account Information:</b>\n\nUsername: {account_info["result"]["login"]}\nPremium Expire: {account_info["result"]["premium_expire"]}\nEmail: {account_info["result"]["email"]}\nTotal Files: {account_info["result"]["files_total"]}\nPremium: {account_info["result"]["premium"]}\nBalance: {account_info["result"]["balance"]}\nStorage Used: {storage_info:.2f} GB\nStorage Left: {account_info["result"]["storage_left"]}\nServer Time: {account_info["server_time"]}')

# account info closed 
@app.on_message(filters.command("accountstats"))
def accountstats(bot,message):
    if message.from_user.id not in approved_users:
        bot.send_message(message.chat.id, "You are not an approved user.\nContact @RoarCyber to get access.")
        return
    else:
        account_stats = get_account_stats()
        clear_screen()
        if "result" in account_stats:
            for item in account_stats["result"]:
                continue
            bot.send_message(message.chat.id, f'<b>Showing Account Stats:</b>\n\nDate: {item["day"]}\nViews: {item["views"]}\nViews (Premium): {item["views_prem"]}\nViews (ADB): {item["views_adb"]}\nSales: {item["sales"]}\nDownloads:{item["downloads"]}\nProfit from Views: {item["profit_views"]}\nProfit from Referrals: {item["profit_refs"]}\nProfit from Site: {item["profit_site"]}\nProfit from Sales: {item["profit_sales"]}\nTotal Profit: {item["profit_total"]}\nRefs: {item["refs"]}')    
        else:
            print("No 'result' field in the response.")


# Run the bot
app.run()

# Telegram Spotify Search Bot
A simple asyncronous bot based on [aiogram](https://github.com/aiogram/aiogram). This bot uses [aiohttp](https://docs.aiohttp.org/en/stable/) for making HTTP requests and [pydantic](https://pydantic-docs.helpmanual.io/) for generating types and dataclass for the HTTP response from spotify.

--- 

## Installation

- Clone this repo or download the zip file.
- Download the requirements: `pip install -r requirements.txt`
- In the [.env](.env) file put your **spotify client id** and **spotify client secret** and put your **telegram bot token** and you/owner's **chat id**.
- Now simply run the [app.py](app.py) script <br>
  `python app.py` for windows.  <br>
  `python3 app.py` for *nix platforms. <br>

--- 

## Getting the spotify credentials

- Browse to the [spotify developer's portal dashboard](https://developer.spotify.com/dashboard/applications).
- Log in with your Spotify account.
- Click on **Create an app**.
- Pick an **App name** and **App description** of your choice and mark the checkboxes.
- After creation, you see your _Client Id_ and you can click on **Show client secret** to unhide your _Client secret_.

---

## Getting the telegram credentials

- Download [telegram desktop app](https://telegram.org/) and create a new account if you don't have one.
- Goto [@BotFather](https://t.me/BotFather) and click **start**
- Send `/newbot` command to make a new bot and copy its _bot token_
- Goto [@MissRose_Bot](https://t.me/MissRose_bot) and click **start**
- Send `/id` command to get your _chat id_

---

## Usage

- `/start` -> To start your bot
- `/search {q}` -> To search your _query_ in spotify

Regards: **[Sirshak Bohara](https://github.com/sirshakbohara)**
# get_chat_id.py
from dotenv import load_dotenv # <--- ADD THIS LINE
load_dotenv() # <--- ADD THIS LINE

from telegram_bot import get_chat_id
from config import Config

if __name__ == "__main__":
    bot_token = Config().TELEGRAM_BOT_TOKEN
    
    if not bot_token: # <--- ADD THIS CHECK
        print("Error: TELEGRAM_BOT_TOKEN not found. Make sure it's in your .env file.")
        exit() # Exit if token is not found

    print(f"Using bot token: {bot_token[:5]}...{bot_token[-5:]}")
    chat_id = get_chat_id(bot_token)
    if chat_id:
        print(f"\nYour chat ID is: {chat_id}")
        print("Copy this and paste it in config.py as TELEGRAM_CHAT_ID")
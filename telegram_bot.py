import requests
import os
import logging
import time
from typing import List

class TelegramSender:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        if not self.bot_token or not self.chat_id:
            raise ValueError("Missing Telegram credentials")
            
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/"
        logging.basicConfig(level=logging.INFO)

    def send_message(self, message: str) -> bool:
        try:
            response = requests.post(
                self.base_url + "sendMessage",
                json={
                    'chat_id': self.chat_id,
                    'text': message,
                    'parse_mode': 'HTML',
                    'disable_web_page_preview': True
                },
                timeout=10
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logging.error(f"Telegram send error: {str(e)}")
            if hasattr(e, 'response') and e.response.text:
                logging.error(f"Telegram API response: {e.response.text}")
            return False

    def send_newsletter(self, messages: List[str]) -> bool:
        """Send multiple message chunks"""
        success = True
        for message in messages:
            if not self.send_message(message):
                success = False
                time.sleep(1)  # Brief pause between attempts
        return success

def get_chat_id(bot_token: str) -> str:
    if not bot_token:
        return None
        
    try:
        response = requests.get(
            f"https://api.telegram.org/bot{bot_token}/getUpdates",
            timeout=10
        )
        data = response.json()
        
        if not data.get('ok'):
            return None
            
        if not data['result']:
            print("Send a message to your bot first")
            return None
            
        last_update = data['result'][-1]
        if 'message' in last_update:
            return str(last_update['message']['chat']['id'])
        elif 'channel_post' in last_update:
            return str(last_update['channel_post']['chat']['id'])
            
    except Exception as e:
        print(f"Error getting chat ID: {str(e)}")
        return None
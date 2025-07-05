import time
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from scraper import NewsScraper
from processor import ArticleProcessor
from telegram_bot import TelegramSender
from config import Config

def test_telegram_connection():
    try:
        sender = TelegramSender()
        test_msg = (
            "<b>✨ Test Message ✨</b>\n"
            "<i>This is a test of the Telegram bot connection.</i>\n"
            "If you see this, the basic setup is working!"
        )
        return sender.send_message(test_msg)
    except Exception as e:
        print(f"Telegram test failed: {str(e)}")
        return False

def main():
    config = Config()
    scraper = NewsScraper()
    processor = ArticleProcessor()
    sender = TelegramSender()

    # Test connection first
    print("Testing Telegram connection...")
    if not test_telegram_connection():
        print("❌ Telegram test failed. Check credentials.")
        return

    # Simulation loop
    for day in range(1, config.SIMULATION_DAYS + 1):
        print(f"\n📅 DAY {day} - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Scrape news
        print("🕸️ Scraping news sources...")
        articles = scraper.scrape_articles()

        if not articles:
            print("No articles to process")
            time.sleep(config.DAILY_DELAY_SECONDS)
            continue

        # Process articles
        print("🧠 Processing articles...")
        processed_articles = processor.process_articles(articles)

        # Send newsletter
        print("📤 Sending newsletter...")
        if processed_articles:
            newsletter_messages = processor.format_newsletter(processed_articles)
            print(f"\nGenerated {len(newsletter_messages)} message chunks")
            
            if sender.send_newsletter(newsletter_messages):
                print("✅ Newsletter sent successfully!")
            else:
                print("❌ Failed to send newsletter")

        time.sleep(config.DAILY_DELAY_SECONDS)

if __name__ == "__main__":
    main()
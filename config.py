#config.py
import os

class Config:
    # Telegram settings
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    # General User Agent for requests (both scraper and newspaper3k)
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

    # NEWS_SOURCES: Only include the working sources for now.
    NEWS_SOURCES = [
        {
            "name": "CoinDesk RSS",
            "url": "https://www.coindesk.com/arc/outboundfeeds/rss/",
            "type": "rss"                       # Really Simple Syndication
        },
        {
            "name": "CoinTelegraph RSS",
            "url": "https://cointelegraph.com/rss",
            "type": "rss"                       # Really Simple Syndication
        },
        # Removing The Block, NewsBTC, Crypto Potato for now.
        # {
        #     "name": "The Block RSS",
        #     "url": "https://www.theblock.co/rss", # Keeping the last attempt URL for reference
        #     "type": "rss"
        # },
        {
            "name": "Bitcoinist",
            "url": "https://bitcoinist.com",
            "scrape_pattern": {
                "container": "article.jeg_post",
                "title": "h3.jeg_post_title a",
                "link": "h3.jeg_post_title a",
                "summary": "div.jeg_post_excerpt p",
                "date": "div.jeg_meta_date a"
            }
        },
        # {
        #      "name": "NewsBTC",
        #      "url": "https://www.newsbtc.com",
        #      "scrape_pattern": {
        #          "container": "article.jeg_post",
        #          "title": "h3.jeg_post_title a",
        #          "link": "h3.jeg_post_title a",
        #          "summary": "div.jeg_post_excerpt p",
        #          "date": "div.jeg_meta_date a"
        #      }
        # },
        # {
        #      "name": "Crypto Potato",
        #      "url": "https://cryptopotato.com",
        #      "scrape_pattern": {
        #          "container": "article.post",
        #          "title": "h2.entry-title a",
        #          "link": "h2.entry-title a",
        #          "summary": "div.entry-summary p",
        #          "date": "span.posted-on time"
        #      }
        # },
        {
            "name": "The Defiant",
            "url": "https://thedefiant.io/feed",
            "type": "rss"
        },
        {
            "name": "CryptoPanic",
            "url": "https://cryptopanic.com/news/rss/",
            "type": "rss",
            "params": {
            "auth_token": "YOUR_API_KEY"  # Optional for more features
        }
}
        
]
    

    # Processing settings
    MAX_ARTICLES_PER_SOURCE = 5
    TOP_ARTICLES_DAILY = 25
    SIMILARITY_THRESHOLD = 0.8

    # Summarization settings
    # The prompt will still be used, but the pipeline handles the actual summarization logic.
    SUMMARIZATION_PROMPT = """Summarize this in 2 sentences:
    Title: {title}
    Content: {content}
    Summary:"""

    # Simulation settings
    SIMULATION_DAYS = 2
    DAILY_DELAY_SECONDS = 5
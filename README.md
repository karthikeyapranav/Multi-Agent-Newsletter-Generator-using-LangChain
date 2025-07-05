# Web3 Newsletter Generator

Automated daily newsletter from top Web3 news sources delivered via Telegram.

## Features
- Scrapes 5+ news sources
- AI-powered summaries
- Deduplication
- Multi-format delivery (HTML/Markdown)
- Scheduled daily updates

## Current Sources
1. CoinDesk (RSS)
2. CoinTelegraph (RSS) 
3. Bitcoinist (Scraped)
4. The Defiant (RSS)
5. CryptoPanic (RSS)

## Setup
1. Clone repo
2. Install requirements: `pip install -r requirements.txt`
3. Configure `.env`:

TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id

4. Run: `python scheduler.py`

## Configuration
Edit `config.py` to:
- Adjust number of articles (`TOP_ARTICLES_DAILY`)
- Add/remove news sources
- Set similarity thresholds

## Troubleshooting
- 403 Errors: Check if source blocks scraping
- Timeouts: Increase timeout in `newspaper_config`
- Partial articles: Verify RSS feed availability


### Adding New Sources
1. RSS Sources:
   ```python
   {
       "name": "SourceName",
       "url": "rss_feed_url",
       "type": "rss"
   }
### HTML Sources: = 
{
    "name": "SourceName",
    "url": "https://example.com",
    "scrape_pattern": {
        "container": "css_selector",
        "title": "css_selector",
        "link": "css_selector",
        "summary": "css_selector",
        "date": "css_selector"
    }
}


### Optimization Tips
Use RSS over HTML scraping when possible

Set realistic timeouts (15-30s)

Cache article summaries for performance

Monitor source rate limits
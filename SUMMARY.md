## System Overview

### Data Flow
1. **Scraping** (scraper.py)
   - RSS feeds fetched via requests
   - HTML content parsed using BeautifulSoup
   - Rate-limited to avoid blocks

2. **Processing** (processor.py)
   - Article deduplication (title similarity)
   - Content summarization (HuggingFace BART model)
   - HTML/Markdown formatting

3. **Delivery** (telegram_bot.py)
   - Chunked messages (5 articles/message)
   - Automatic retries on failure
   - HTML formatting for rich previews

### Key Configurations
- `MAX_ARTICLES_PER_SOURCE`: Limits per-source scraping
- `SIMILARITY_THRESHOLD`: Title deduplication sensitivity  
- `DAILY_DELAY_SECONDS`: Simulated days duration


###  Additional Recommendations

1. **For CryptoPanic API**:
   - Register at https://cryptopanic.com/developers/
   - Free tier allows 30 requests/minute
   - Provides sentiment data (bullish/bearish indicators)

2. **Error Handling Improvements**:
```python
# In scraper.py
def safe_request(self, url, is_rss=False):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/rss+xml' if is_rss else 'text/html'
        }
        response = self.session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.content if is_rss else BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"⚠️ Error accessing {url}: {str(e)}")
        return None   
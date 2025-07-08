# 📰 Web3 Daily Digest: Automated Newsletter Generator

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![AI Powered](https://img.shields.io/badge/AI%20Powered-Summarization-FF69B4.svg)](https://en.wikipedia.org/wiki/Natural_language_processing)
[![Telegram Delivery](https://img.shields.io/badge/Telegram-Bot%20API-0088CC.svg?logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)
[![Scheduled Jobs](https://img.shields.io/badge/Scheduler-Daily%20Updates-orange.svg)](https://pypi.org/project/schedule/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Welcome to the **Web3 Daily Digest**, an automated solution designed to keep you at the forefront of the rapidly evolving Web3 space. This project intelligently scrapes, summarizes, and delivers the most important daily news from top Web3 and cryptocurrency sources directly to your Telegram chat. Say goodbye to information overload and hello to concise, AI-powered daily insights!

---

## ✨ Key Features

This newsletter generator is packed with functionalities to ensure you receive timely, relevant, and easy-to-digest news:

* **Diverse News Source Integration:** Gathers articles from a curated list of leading Web3 and crypto news outlets, utilizing both efficient RSS feeds and robust HTML web scraping where RSS is unavailable.
* **AI-Powered Summarization:** Leverages the power of large language models (LLMs) to generate succinct and informative summaries for each article, allowing you to grasp key points at a glance.
* **Intelligent Deduplication:** Employs similarity thresholds to identify and filter out duplicate or highly similar articles across different sources, ensuring you don't receive redundant information.
* **Flexible Multi-Format Delivery:** Generates newsletters in both HTML and Markdown formats, offering versatility for various consumption platforms. Currently optimized for rich display within Telegram.
* **Automated Daily Scheduling:** Configured to run automatically once a day, delivering your personalized Web3 digest without any manual intervention.
* **Customizable Content:** Easily adjust the number of top articles, manage news sources, and fine-tune AI summarization parameters.

---

## 📡 Current News Sources

We prioritize a mix of reliable RSS feeds for efficiency and targeted HTML scraping for sources without comprehensive feeds.

1.  **CoinDesk:** (RSS Feed) - A leading source for cryptocurrency news, price, and information.
2.  **CoinTelegraph:** (RSS Feed) - Offers news, analysis, and reviews on blockchain technology, cryptocurrencies, and fintech.
3.  **Bitcoinist:** (HTML Scraped) - Provides news and analysis covering Bitcoin, altcoins, and blockchain. *(Note: This source requires direct HTML scraping due to limited RSS feed content).*
4.  **The Defiant:** (RSS Feed) - Focuses on decentralized finance (DeFi) news and trends.
5.  **CryptoPanic:** (RSS Feed) - An aggregator that collects news from various crypto sources.

---

## ⚙️ Setup & Quick Start

Getting your daily Web3 newsletter up and running is quick and easy!

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/Web3-Newsletter-Generator.git](https://github.com/your-username/Web3-Newsletter-Generator.git)
    cd Web3-Newsletter-Generator
    ```

2.  **Install Python Dependencies:**
    All required libraries are listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory of the project and populate it with your Telegram Bot Token and Chat ID.
    * **`TELEGRAM_BOT_TOKEN`**: Obtain this by creating a new bot with `@BotFather` on Telegram.
    * **`TELEGRAM_CHAT_ID`**: Get your chat ID by forwarding a message from your desired chat to `@getidsbot` or similar.

    ```dotenv
    TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE
    TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID_HERE
    # Optional: If using a paid AI service, add your API key here
    # OPENAI_API_KEY=sk-your_openai_api_key
    ```

4.  **Run the Scheduler:**
    This script will set up the daily job to fetch news, process it, and send the newsletter.
    ```bash
    python scheduler.py
    ```
    The newsletter will now be delivered to your specified Telegram chat daily.

---

## 🔧 Advanced Configuration

The `config.py` file provides extensive options for customizing your newsletter:

* **`TOP_ARTICLES_DAILY`**: Adjust the maximum number of articles to include in each daily newsletter.
* **Adding/Removing News Sources:**
    * You can easily modify the `NEWS_SOURCES` list to include new sources or remove existing ones.
    * **For RSS Feeds:**
        ```python
        {
            "name": "NewRSSSource",
            "url": "[https://newsource.com/rss_feed.xml](https://newsource.com/rss_feed.xml)",
            "type": "rss"
        }
        ```
    * **For HTML Scraped Sources:**
        * This requires defining specific CSS selectors to accurately extract content. Use browser developer tools to identify these.
        * `container`: CSS selector for the main article block.
        * `title`: CSS selector for the article's title.
        * `link`: CSS selector for the article's URL.
        * `summary`: CSS selector for the article's summary/excerpt (if available on the listing page).
        * `date`: CSS selector for the article's publication date.
        ```python
        {
            "name": "NewHTMLSource",
            "url": "[https://newsource.com/news](https://newsource.com/news)",
            "type": "html",
            "scrape_pattern": {
                "container": "article.news-item",
                "title": "h2.article-title a",
                "link": "h2.article-title a",
                "summary": "p.article-summary",
                "date": "span.article-date"
            }
        }
        ```
* **Similarity Thresholds (`DEDUPLICATION_THRESHOLD`)**: Fine-tune the sensitivity of the deduplication algorithm. A higher value means articles need to be more similar to be considered duplicates.
* **AI Model Selection:** If using a language model, configure the model name and any specific parameters.

---

## 🪲 Troubleshooting Common Issues

Encountering issues? Here are some common problems and their solutions:

* **`403 Forbidden` Errors when Scraping HTML:**
    * **Cause:** The target website might be actively blocking automated scraping (e.g., detecting `User-Agent` headers or frequent requests).
    * **Solution:**
        * Try rotating `User-Agent` headers (though not explicitly implemented in this basic setup).
        * Introduce longer `time.sleep()` delays between requests to that specific source in the scraping logic.
        * Consider using a proxy service if the issue persists and the data is critical.
        * *Best Practice:* Always check the website's `robots.txt` file and Terms of Service before scraping.
* **Timeouts During Article Fetching:**
    * **Cause:** The server hosting the news source might be slow to respond, or your network connection might be unstable.
    * **Solution:** Increase the `timeout` parameter within the `newspaper_config` (if using `newspaper3k`) or any `requests` calls for HTML sources.
* **Partial Articles or Missing Content:**
    * **Cause:** The RSS feed might be truncated, or the HTML scraping selectors are incorrect/outdated, failing to capture the full article content.
    * **Solution:**
        * **For RSS:** Verify the RSS feed URL directly in your browser to ensure it's providing full content.
        * **For HTML:** Re-inspect the website's HTML structure using browser developer tools and update the `scrape_pattern` selectors in `config.py` accordingly. Websites frequently update their layouts, which can break scrapers.
* **Newsletter Not Sending:**
    * **Cause:** Incorrect `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` in your `.env` file, or a network issue preventing connection to Telegram API.
    * **Solution:** Double-check your environment variables. Test your Telegram Bot token directly with a simple API call if unsure.

---

## ⚡ Optimization & Best Practices

To ensure efficient and ethical scraping, consider these tips:

* **Prioritize RSS Over HTML Scraping:** RSS feeds are designed for content syndication, are less resource-intensive, and less likely to be blocked. Use HTML scraping only when a robust RSS feed is unavailable.
* **Set Realistic Timeouts:** Don't let your script hang indefinitely. Use timeouts (e.g., 15-30 seconds) for network requests.
* **Implement Caching:** For AI summaries or frequently accessed data, implement a simple caching mechanism to reduce API calls and processing time.
* **Monitor Source Rate Limits:** Be mindful of how frequently you hit a particular news source. Overly aggressive scraping can lead to IP bans or temporary blocks. Introduce delays (`time.sleep()`) between requests to the same domain.
* **Error Handling and Logging:** Implement robust `try-except` blocks around network requests and processing steps. Log errors comprehensively to quickly diagnose issues.

---

## 📈 Future Enhancements

This project can be further enhanced with more advanced features:

* **Persistence for Read Articles:** Store a list of articles already sent to prevent sending them again in future digests, even if they reappear on news feeds.
* **Sentiment Analysis:** Integrate natural language processing (NLP) to determine the sentiment (positive, negative, neutral) of articles.
* **User Preferences & Filters:** Allow users to customize topics of interest, preferred sources, or even keywords to include/exclude.
* **Multiple Channel/User Support:** Extend the Telegram integration to send newsletters to multiple chats or individual users based on their preferences.
* **Database Integration:** Instead of just sending a daily newsletter, store all scraped articles in a local database (e.g., SQLite, PostgreSQL) for historical analysis and searchability.
* **Web Interface (Optional):** Develop a simple web UI to manage sources, view historical newsletters, and configure settings.
* **More Advanced AI Summarization:** Explore different LLM models or fine-tuning techniques for even more nuanced summaries.

---

## 🤝 Contribution

Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is open-sourced under the [MIT License](LICENSE).

import os
from datetime import datetime
from transformers import pipeline
from config import Config
from typing import List, Dict
from newspaper import Article, Config as NewspaperConfig

class ArticleProcessor:
    def __init__(self):
        self.config = Config()
        self.summarizer_pipeline = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
        )
        self.newspaper_config = NewspaperConfig()
        self.newspaper_config.browser_user_agent = self.config.USER_AGENT
        self.newspaper_config.request_timeout = 15

    def _escape_html(self, text: str) -> str:
        """Escape all HTML special characters"""
        if not text:
            return ""
        escapes = [
            ("&", "&amp;"),
            ("<", "&lt;"),
            (">", "&gt;"),
            ('"', "&quot;"),
            ("'", "&apos;")
        ]
        for char, escape in escapes:
            text = text.replace(char, escape)
        return text

    def get_full_article_content(self, url: str) -> str:
        try:
            article = Article(url, config=self.newspaper_config)
            article.download()
            article.parse()
            return article.text
        except Exception as e:
            print(f"⚠️ Error downloading article: {str(e)}")
            return ""

    def summarize_article(self, article_data: Dict) -> str:
        full_content = self.get_full_article_content(article_data['link'])
        if not full_content:
            return "Failed to summarize: Content not available."

        max_chars = 4000
        if len(full_content) > max_chars:
            full_content = full_content[:max_chars] + "..."

        try:
            summaries = self.summarizer_pipeline(
                full_content,
                max_length=150,
                min_length=50,
                do_sample=False
            )
            return summaries[0]['summary_text'].strip()
        except Exception as e:
            print(f"⚠️ Summarization error: {str(e)}")
            return "Failed to summarize."

    def process_articles(self, articles: List[Dict]) -> List[Dict]:
        processed = []
        unique_titles = set()

        for article in articles:
            if article['title'] in unique_titles:
                continue
            unique_titles.add(article['title'])

            summary = self.summarize_article(article)
            if summary and "Failed to summarize" not in summary:
                article['ai_summary'] = summary
                processed.append(article)

            if len(processed) >= self.config.TOP_ARTICLES_DAILY:
                break
        
        return processed

    def format_newsletter(self, articles: List[Dict]) -> List[str]:
        if not articles:
            return ["<b>No relevant news today. Stay tuned for updates!</b>"]

        # Split articles into chunks of 5
        chunks = [articles[i:i+5] for i in range(0, len(articles), 5)]
        messages = []
        
        for chunk_idx, chunk in enumerate(chunks):
            # Header (only for first chunk)
            if chunk_idx == 0:
                message = (
                    "<b>✨ Daily Web3 News Digest ✨</b>\n"
                    f"<i>📅 Date: {datetime.now().strftime('%Y-%m-%d')}</i>\n"
                    "--------------------------------\n\n"
                )
            else:
                message = f"<b>✨ Continued ({chunk_idx+1}/{len(chunks)}) ✨</b>\n\n"
            
            # Add articles
            for i, article in enumerate(chunk):
                article_num = chunk_idx * 5 + i + 1
                title = self._escape_html(article['title'])
                source = self._escape_html(article['source'])
                date = self._escape_html(article.get('date', 'N/A'))
                summary = self._escape_html(article['ai_summary'])
                link = article['link']
                
                message += (
                    f"<b>{article_num}. {title}</b>\n"
                    f"<i>{source} - {date}</i>\n"
                    f"{summary}\n"
                    f'<a href="{link}">Read More</a>\n'
                    "--------------------------------\n\n"
                )
            
            # Footer (only for last chunk)
            if chunk_idx == len(chunks) - 1:
                message += (
                    "💡 <i>Want more? Reply with feedback!</i>\n"
                    "<i>Powered by Web3News AI</i>"
                )
            
            messages.append(message)
        
        return messages
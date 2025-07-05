#newsletter.py
from datetime import datetime
from typing import List, Dict

class NewsletterComposer:
    def __init__(self):
        self.date = datetime.now().strftime("%B %d, %Y")
    
    def compose(self, articles: List[Dict]) -> str:
        if not articles:
            return "⚠️ No articles found today. Check back tomorrow!"
            
        # Header
        newsletter = f"🚀 *Web3 Daily - {self.date}*\n\n"
        newsletter += "Top crypto news curated for you:\n\n---\n\n"
        
        # Group by source
        sources = {}
        for article in articles:
            if article['source'] not in sources:
                sources[article['source']] = []
            sources[article['source']].append(article)
        
        # Add articles
        for source, items in sources.items():
            newsletter += f"*📌 {source}*\n"
            for article in items:
                newsletter += (
                    f"• *{article['title']}*\n"
                    f"{article['ai_summary']}\n"
                    f"[Read more]({article['link']})\n\n"
                )
        
        # Footer
        newsletter += (
            "---\n\n"
            "💡 Want more? Reply with feedback!\n"
            "Powered by Web3News AI | [Suggest Sources](https://t.me/yourchannel)"
        )
        
        return newsletter
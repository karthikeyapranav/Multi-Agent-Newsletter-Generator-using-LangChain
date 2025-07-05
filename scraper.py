# scraper.py (No changes from previous version)
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from config import Config
import time
import random
import xml.etree.ElementTree as ET # For RSS parsing

class NewsScraper:
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        self.headers = {
            'User-Agent': self.config.USER_AGENT, # <--- Uses the common USER_AGENT from config
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        }

    def safe_request(self, url, is_rss=False):
        try:
            time.sleep(random.uniform(1, 3)) # Be polite
            response = self.session.get(url, headers=self.headers, timeout=30)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            if is_rss:
                return response.content # Return raw content for XML parsing
            else:
                return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Network/Request Error accessing {url}: {str(e)}")
            return None
        except Exception as e:
            print(f"⚠️ Unexpected Error during request to {url}: {str(e)}")
            return None

    def scrape_html_source(self, source: Dict) -> List[Dict]:
        soup = self.safe_request(source['url'])
        if not soup:
            return []
            
        articles = []
        try:
            containers = soup.select(source['scrape_pattern']['container'])
            
            for article_element in containers[:self.config.MAX_ARTICLES_PER_SOURCE]:
                try:
                    title_element = article_element.select_one(source['scrape_pattern']['title'])
                    link_element = article_element.select_one(source['scrape_pattern']['link'])
                    summary_element = article_element.select_one(source['scrape_pattern']['summary'])
                    date_element = article_element.select_one(source['scrape_pattern']['date'])

                    title = title_element.text.strip() if title_element else "No Title"
                    link = link_element['href'] if link_element and 'href' in link_element.attrs else source['url']
                    
                    if not link.startswith('http'):
                        link = f"{source['url'].rstrip('/')}{link}" if link.startswith('/') else f"{source['url']}/{link}"
                    
                    summary = summary_element.text.strip() if summary_element else ""
                    date = date_element.text.strip() if date_element else ""
                    
                    articles.append({
                        'title': title,
                        'link': link,
                        'summary': summary,
                        'source': source['name'],
                        'date': date
                    })
                except Exception as e:
                    print(f"⚠️ Error parsing individual article from {source['name']}: {str(e)}")
                    continue
        except Exception as e:
            print(f"⚠️ Error selecting containers from {source['name']}: {str(e)}")
            return []
                
        return articles

    def scrape_rss_source(self, source: Dict) -> List[Dict]:
        rss_content = self.safe_request(source['url'], is_rss=True)
        if not rss_content:
            return []

        articles = []
        try:
            root = ET.fromstring(rss_content)
            items = root.findall(".//item") or root.findall(".//entry") # Support both RSS and Atom
            
            for item in items[:self.config.MAX_ARTICLES_PER_SOURCE]:
                try:
                    title_element = item.find("title")
                    link_element = item.find("link")
                    description_element = item.find("description") or item.find("summary") # Atom uses summary
                    pub_date_element = item.find("pubDate") or item.find("updated") # Atom uses updated
                    
                    title = title_element.text.strip() if title_element is not None and title_element.text else "No Title"
                    
                    link = ""
                    if link_element is not None:
                        if link_element.text and link_element.text.strip().startswith('http'): # For RSS <link>
                            link = link_element.text.strip()
                        elif link_element.attrib.get('href'): # For Atom <link href="...">
                            link = link_element.attrib.get('href').strip()
                    
                    summary = description_element.text.strip() if description_element is not None and description_element.text else ""
                    date = pub_date_element.text.strip() if pub_date_element is not None and pub_date_element.text else ""

                    articles.append({
                        'title': title,
                        'link': link,
                        'summary': summary,
                        'source': source['name'],
                        'date': date
                    })
                except Exception as e:
                    print(f"⚠️ Error parsing individual RSS item from {source['name']}: {str(e)}")
                    continue
        except ET.ParseError as e:
            print(f"⚠️ Error parsing RSS/XML content from {source['name']}: {str(e)}")
            return []
        except Exception as e:
            print(f"⚠️ Unexpected error during RSS parsing for {source['name']}: {str(e)}")
            return []
                
        return articles


    def scrape_articles(self) -> List[Dict]:
        all_articles = []
        for source in self.config.NEWS_SOURCES:
            print(f"🌐 Scraping {source['name']}...")
            articles = []
            if source.get('type') == 'rss':
                articles = self.scrape_rss_source(source)
            else:
                articles = self.scrape_html_source(source)

            if articles:
                print(f"✅ Found {len(articles)} articles from {source['name']}")
                all_articles.extend(articles)
            else:
                print(f"❌ No articles found from {source['name']}.")
            
        print(f"\n✨ Total articles scraped: {len(all_articles)}")
        return all_articles
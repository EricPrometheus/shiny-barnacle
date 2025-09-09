"""
Simple RSS feed parser without external dependencies
"""

import re
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleRSSParser:
    """Basic RSS feed parser using built-in XML parser"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def parse_feed(self, feed_url: str) -> List[Dict]:
        """Parse RSS feed and return list of articles"""
        try:
            logger.info(f"Parsing RSS feed: {feed_url}")
            
            response = self.session.get(feed_url, timeout=30)
            response.raise_for_status()
            
            # Parse XML
            root = ET.fromstring(response.content)
            
            articles = []
            
            # Find all item elements
            items = root.findall('.//item')
            
            for item in items:
                article = {}
                
                # Extract basic fields
                title_elem = item.find('title')
                article['title'] = title_elem.text if title_elem is not None else 'No title'
                
                link_elem = item.find('link')
                article['link'] = link_elem.text if link_elem is not None else ''
                
                description_elem = item.find('description')
                if description_elem is not None:
                    # Clean HTML from description
                    desc = description_elem.text or ''
                    desc = re.sub(r'<[^>]+>', '', desc)  # Remove HTML tags
                    desc = desc.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                    article['description'] = desc.strip()
                else:
                    article['description'] = ''
                
                pubdate_elem = item.find('pubDate')
                article['published'] = pubdate_elem.text if pubdate_elem is not None else ''
                
                article['source'] = 'BBC News'
                
                articles.append(article)
            
            logger.info(f"Parsed {len(articles)} articles from {feed_url}")
            return articles
            
        except Exception as e:
            logger.error(f"Error parsing RSS feed {feed_url}: {e}")
            return []


# Update the news_fetcher.py to use simple RSS parser as fallback
class SimpleBBCNewsFetcher:
    """BBC News fetcher using simple RSS parser"""
    
    def __init__(self):
        self.rss_feeds = [
            "http://feeds.bbci.co.uk/news/technology/rss.xml",
            "http://feeds.bbci.co.uk/news/business/rss.xml", 
            "http://feeds.bbci.co.uk/news/world/rss.xml"
        ]
        self.rss_parser = SimpleRSSParser()
        self.ai_keywords = [
            "artificial intelligence", "ai", "machine learning", "ml", "deep learning",
            "neural network", "chatgpt", "gpt", "openai", "google ai", "deepmind", 
            "autonomous", "automation", "robot", "algorithm", "data science",
            "computer vision", "natural language", "nlp", "generative ai",
            "large language model", "llm", "transformer", "bert", "claude",
            "anthropic", "microsoft ai", "meta ai", "nvidia ai"
        ]
    
    def is_ai_related(self, article: Dict) -> bool:
        """Check if article is AI-related"""
        text_to_check = f"{article['title']} {article['description']}".lower()
        
        for keyword in self.ai_keywords:
            if keyword.lower() in text_to_check:
                return True
        return False
    
    def filter_today_news(self, articles: List[Dict]) -> List[Dict]:
        """Filter for today's articles (simplified)"""
        # For simplicity, return all articles as RSS feeds usually contain recent news
        return articles
    
    def fetch_ai_news(self, today_only: bool = True) -> List[Dict]:
        """Fetch AI-related news from BBC RSS feeds"""
        all_articles = []
        
        # Fetch from all RSS feeds
        for feed_url in self.rss_feeds:
            articles = self.rss_parser.parse_feed(feed_url)
            all_articles.extend(articles)
        
        # Filter for AI-related content
        ai_articles = [article for article in all_articles if self.is_ai_related(article)]
        logger.info(f"Found {len(ai_articles)} AI-related articles out of {len(all_articles)} total")
        
        # Remove duplicates based on title
        seen_titles = set()
        unique_articles = []
        for article in ai_articles:
            if article['title'] not in seen_titles:
                seen_titles.add(article['title'])
                unique_articles.append(article)
        
        logger.info(f"Final count: {len(unique_articles)} unique AI articles")
        return unique_articles


if __name__ == "__main__":
    fetcher = SimpleBBCNewsFetcher()
    articles = fetcher.fetch_ai_news()
    for article in articles[:3]:  # Show first 3
        print(f"Title: {article['title']}")
        print(f"Link: {article['link']}")
        print(f"Description: {article['description'][:100]}...")
        print("-" * 50)
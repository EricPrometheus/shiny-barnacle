"""
BBC News fetcher module for AI news aggregation
"""

import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import logging

from config import BBC_TECH_RSS, BBC_BUSINESS_RSS, BBC_WORLD_RSS, AI_KEYWORDS, REQUEST_TIMEOUT, USER_AGENT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BBCNewsFetcher:
    """Fetches and filters AI-related news from BBC RSS feeds"""
    
    def __init__(self):
        self.rss_feeds = [BBC_TECH_RSS, BBC_BUSINESS_RSS, BBC_WORLD_RSS]
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        self.ai_keywords = [keyword.lower() for keyword in AI_KEYWORDS]
    
    def fetch_rss_feed(self, feed_url: str) -> List[Dict]:
        """Fetch articles from a single RSS feed"""
        try:
            logger.info(f"Fetching RSS feed: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            articles = []
            for entry in feed.entries:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': 'BBC News'
                }
                articles.append(article)
            
            logger.info(f"Found {len(articles)} articles from {feed_url}")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching RSS feed {feed_url}: {e}")
            return []
    
    def is_ai_related(self, article: Dict) -> bool:
        """Check if an article is AI-related based on keywords"""
        text_to_check = f"{article['title']} {article['description']}".lower()
        
        for keyword in self.ai_keywords:
            if keyword in text_to_check:
                return True
        return False
    
    def filter_today_news(self, articles: List[Dict]) -> List[Dict]:
        """Filter articles published today"""
        today = datetime.now().date()
        filtered_articles = []
        
        for article in articles:
            try:
                # Parse the published date
                pub_date = datetime.strptime(article['published'], '%a, %d %b %Y %H:%M:%S %Z').date()
                if pub_date == today:
                    filtered_articles.append(article)
            except:
                # If date parsing fails, include the article (better to be inclusive)
                filtered_articles.append(article)
        
        return filtered_articles
    
    def fetch_ai_news(self, today_only: bool = True) -> List[Dict]:
        """Fetch AI-related news from all BBC RSS feeds"""
        all_articles = []
        
        # Fetch from all RSS feeds
        for feed_url in self.rss_feeds:
            articles = self.fetch_rss_feed(feed_url)
            all_articles.extend(articles)
        
        # Filter for AI-related content
        ai_articles = [article for article in all_articles if self.is_ai_related(article)]
        logger.info(f"Found {len(ai_articles)} AI-related articles out of {len(all_articles)} total articles")
        
        # Filter for today's news if requested
        if today_only:
            ai_articles = self.filter_today_news(ai_articles)
            logger.info(f"Filtered to {len(ai_articles)} articles from today")
        
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
    fetcher = BBCNewsFetcher()
    news = fetcher.fetch_ai_news()
    for article in news:
        print(f"Title: {article['title']}")
        print(f"Link: {article['link']}")
        print("-" * 50)
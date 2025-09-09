"""
Article content extractor and processor
"""

import requests
from newspaper import Article
import logging
from typing import Dict, Optional
from config import REQUEST_TIMEOUT, USER_AGENT, MIN_ARTICLE_LENGTH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArticleExtractor:
    """Extracts full content from article URLs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
    
    def extract_content(self, url: str) -> Optional[Dict]:
        """Extract full article content from URL"""
        try:
            logger.info(f"Extracting content from: {url}")
            
            # Use newspaper3k for content extraction
            article = Article(url)
            article.download()
            article.parse()
            
            # Get article content
            content = {
                'title': article.title,
                'text': article.text,
                'authors': article.authors,
                'publish_date': article.publish_date,
                'top_image': article.top_image,
                'url': url
            }
            
            # Validate content length
            if len(content['text']) < MIN_ARTICLE_LENGTH:
                logger.warning(f"Article too short: {len(content['text'])} characters")
                return None
            
            logger.info(f"Successfully extracted article: {len(content['text'])} characters")
            return content
            
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}")
            return None
    
    def extract_multiple(self, articles: list) -> list:
        """Extract content from multiple articles"""
        extracted_articles = []
        
        for article in articles:
            content = self.extract_content(article['link'])
            if content:
                # Merge with original article metadata
                enhanced_article = {**article, **content}
                extracted_articles.append(enhanced_article)
        
        logger.info(f"Successfully extracted content from {len(extracted_articles)}/{len(articles)} articles")
        return extracted_articles


if __name__ == "__main__":
    extractor = ArticleExtractor()
    test_url = "https://www.bbc.com/news/technology"
    content = extractor.extract_content(test_url)
    if content:
        print(f"Title: {content['title']}")
        print(f"Text length: {len(content['text'])}")
    else:
        print("Failed to extract content")
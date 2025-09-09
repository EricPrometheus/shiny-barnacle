"""
Simplified content extractor using basic HTTP requests and regex
"""

import requests
import re
import logging
from typing import Dict, Optional
from urllib.parse import urljoin, urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleContentExtractor:
    """Basic content extraction from web pages"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract_text_from_html(self, html: str) -> str:
        """Extract text content from HTML using regex"""
        if not html:
            return ""
        
        # Remove script and style elements
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def extract_content(self, url: str) -> Optional[Dict]:
        """Extract content from a URL"""
        try:
            logger.info(f"Fetching content from: {url}")
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            html = response.text
            
            # Extract title
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else "No title"
            
            # Clean up title
            title = re.sub(r'\s*-\s*BBC.*$', '', title)  # Remove BBC suffix
            title = title.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            
            # Extract main content
            text = self.extract_text_from_html(html)
            
            # Try to find the main article content (BBC-specific patterns)
            article_patterns = [
                r'<div[^>]*data-component="text-block"[^>]*>(.*?)</div>',
                r'<div[^>]*class="[^"]*story-body[^"]*"[^>]*>(.*?)</div>',
                r'<article[^>]*>(.*?)</article>',
                r'<div[^>]*class="[^"]*article[^"]*"[^>]*>(.*?)</div>'
            ]
            
            article_content = ""
            for pattern in article_patterns:
                matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
                if matches:
                    article_content = ' '.join(matches)
                    break
            
            if article_content:
                text = self.extract_text_from_html(article_content)
            
            # If text is still too short, try to get paragraph content
            if len(text) < 200:
                paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL | re.IGNORECASE)
                if paragraphs:
                    text = ' '.join([self.extract_text_from_html(p) for p in paragraphs])
            
            # Basic content validation
            if len(text) < 100:
                logger.warning(f"Extracted content too short: {len(text)} characters")
                return None
            
            content = {
                'title': title,
                'text': text,
                'url': url,
                'authors': ['BBC News'],  # Default for BBC
                'publish_date': None,
                'top_image': None
            }
            
            logger.info(f"Successfully extracted content: {len(text)} characters")
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
            else:
                # Keep original article even if content extraction failed
                extracted_articles.append(article)
        
        logger.info(f"Successfully extracted content from {len(extracted_articles)} articles")
        return extracted_articles


if __name__ == "__main__":
    extractor = SimpleContentExtractor()
    # Test with a simple webpage
    test_url = "https://httpbin.org/html"  
    content = extractor.extract_content(test_url)
    if content:
        print(f"Title: {content['title']}")
        print(f"Text length: {len(content['text'])}")
        print(f"Text preview: {content['text'][:200]}...")
    else:
        print("Failed to extract content")
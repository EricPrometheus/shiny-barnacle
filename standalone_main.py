#!/usr/bin/env python3
"""
BBC News AI Aggregator - Standalone Version

This version works entirely with Python standard library,
no external dependencies required.

Usage:
    python standalone_main.py [options]
"""

import sys
import os
import json
import re
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import urllib.error
import logging
from datetime import datetime
from collections import Counter
from typing import List, Dict, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class StandaloneRSSParser:
    """RSS parser using only standard library"""
    
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    
    def fetch_feed(self, url: str) -> str:
        """Fetch RSS feed content"""
        try:
            req = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return ""
    
    def parse_feed(self, feed_url: str) -> List[Dict]:
        """Parse RSS feed and return articles"""
        try:
            logger.info(f"Parsing RSS feed: {feed_url}")
            
            content = self.fetch_feed(feed_url)
            if not content:
                return []
            
            root = ET.fromstring(content)
            articles = []
            
            # Find all item elements
            items = root.findall('.//item')
            
            for item in items:
                article = {}
                
                # Extract fields
                title_elem = item.find('title')
                article['title'] = title_elem.text if title_elem is not None else 'No title'
                
                link_elem = item.find('link')
                article['link'] = link_elem.text if link_elem is not None else ''
                
                description_elem = item.find('description')
                if description_elem is not None:
                    desc = description_elem.text or ''
                    desc = re.sub(r'<[^>]+>', '', desc)  # Remove HTML
                    desc = desc.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                    article['description'] = desc.strip()
                else:
                    article['description'] = ''
                
                pubdate_elem = item.find('pubDate')
                article['published'] = pubdate_elem.text if pubdate_elem is not None else ''
                
                article['source'] = 'BBC News'
                articles.append(article)
            
            logger.info(f"Parsed {len(articles)} articles")
            return articles
            
        except Exception as e:
            logger.error(f"Error parsing RSS feed: {e}")
            return []


class StandaloneSummarizer:
    """Basic summarizer using standard library only"""
    
    def __init__(self):
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'would', 'i', 'you', 'we', 'they',
            'this', 'these', 'those', 'what', 'where', 'when', 'who', 'why',
            'how', 'said', 'says', 'can', 'could', 'should', 'may', 'might'
        }
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        text = re.sub(r'[^\w\s]', '', text.lower())
        words = text.split()
        keywords = [word for word in words 
                   if word not in self.stop_words and len(word) > 3]
        word_counts = Counter(keywords)
        return [word for word, count in word_counts.most_common(10)]
    
    def summarize_text(self, text: str, max_sentences: int = 2) -> str:
        """Simple text summarization"""
        if not text or len(text) < 100:
            return text
        
        sentences = re.split(r'[.!?]+', text)
        if len(sentences) <= max_sentences:
            return text
        
        # Score sentences by position and keyword density
        keywords = self.extract_keywords(text)
        scored_sentences = []
        
        for i, sentence in enumerate(sentences):
            if len(sentence.strip()) < 20:
                continue
            
            score = 0
            sentence_lower = sentence.lower()
            
            # Score by keywords
            for keyword in keywords:
                score += sentence_lower.count(keyword)
            
            # Bonus for AI terms
            ai_terms = ['ai', 'artificial intelligence', 'machine learning', 'technology']
            for term in ai_terms:
                if term in sentence_lower:
                    score += 2
            
            # Bonus for early sentences
            if i < 3:
                score += 1
            
            scored_sentences.append((sentence.strip(), score, i))
        
        # Select top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        selected = scored_sentences[:max_sentences]
        selected.sort(key=lambda x: x[2])  # Restore order
        
        summary = '. '.join([s[0] for s in selected])
        if summary and not summary.endswith(('.', '!', '?')):
            summary += '.'
        
        return summary
    
    def create_overall_summary(self, articles: List[Dict]) -> str:
        """Create overall summary"""
        if not articles:
            return "No AI news found for today."
        
        # Count topics
        topic_counts = {}
        for article in articles:
            text = f"{article.get('title', '')} {article.get('description', '')}".lower()
            
            if any(word in text for word in ['health', 'medical', 'hospital']):
                topic_counts['Healthcare'] = topic_counts.get('Healthcare', 0) + 1
            elif any(word in text for word in ['business', 'company', 'investment']):
                topic_counts['Business'] = topic_counts.get('Business', 0) + 1
            elif any(word in text for word in ['chatgpt', 'openai', 'language model']):
                topic_counts['Language Models'] = topic_counts.get('Language Models', 0) + 1
            else:
                topic_counts['General AI'] = topic_counts.get('General AI', 0) + 1
        
        summary = f"Found {len(articles)} AI-related articles from BBC News today"
        
        if topic_counts:
            topics = [f"{topic} ({count})" for topic, count in 
                     sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)]
            summary += f". Main topics: {', '.join(topics[:3])}"
        
        return summary + "."


class StandaloneOutputGenerator:
    """Generate output files using standard library"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_json_output(self, articles: List[Dict], overall_summary: str) -> str:
        """Generate JSON output"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_news_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        data = {
            "generation_time": datetime.now().isoformat(),
            "total_articles": len(articles),
            "overall_summary": overall_summary,
            "articles": articles
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Generated JSON: {filepath}")
        return filepath
    
    def generate_html_output(self, articles: List[Dict], overall_summary: str) -> str:
        """Generate HTML output"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_news_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>BBC AI News - {today}</title>
<style>
body{{font-family:Arial,sans-serif;max-width:800px;margin:0 auto;padding:20px;background:#f5f5f5}}
.header{{background:#bb1919;color:white;padding:20px;text-align:center;margin-bottom:30px}}
.summary{{background:#e8f4f8;padding:20px;border-left:5px solid #007cba;margin-bottom:30px}}
.article{{background:white;padding:20px;margin-bottom:20px;border-radius:5px;box-shadow:0 2px 5px rgba(0,0,0,0.1)}}
.title{{color:#bb1919;font-size:1.3em;font-weight:bold;margin-bottom:10px}}
.meta{{color:#666;font-size:0.9em;margin-bottom:15px}}
.link{{color:#007cba;text-decoration:none;font-weight:bold}}
</style></head><body>
<div class="header"><h1>BBC AI News Summary</h1><p>{today}</p></div>
<div class="summary"><h2>📊 Summary ({len(articles)} articles)</h2><p>{overall_summary}</p></div>
<div><h2>📰 Articles</h2>"""
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'No title')
            desc = article.get('description', 'No description')
            link = article.get('link', '#')
            published = article.get('published', 'Unknown date')
            
            html += f"""<div class="article">
<div class="title">{i}. {title}</div>
<div class="meta">📅 {published}</div>
<p>{desc}</p>
<a href="{link}" target="_blank" class="link">Read full article →</a>
</div>"""
        
        html += f"""</div>
<div style="text-align:center;margin-top:40px;color:#666;font-size:0.9em">
Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}
</div></body></html>"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"Generated HTML: {filepath}")
        return filepath


class StandaloneAINewsAggregator:
    """Main aggregator class"""
    
    def __init__(self):
        self.rss_parser = StandaloneRSSParser()
        self.summarizer = StandaloneSummarizer()
        self.output_generator = StandaloneOutputGenerator()
        
        self.rss_feeds = [
            "http://feeds.bbci.co.uk/news/technology/rss.xml",
            "http://feeds.bbci.co.uk/news/business/rss.xml"
        ]
        
        self.ai_keywords = [
            "artificial intelligence", "ai", "machine learning", "ml", "deep learning",
            "neural network", "chatgpt", "gpt", "openai", "google ai",
            "autonomous", "automation", "robot", "algorithm", "data science",
            "computer vision", "natural language", "nlp", "generative ai",
            "large language model", "llm", "transformer", "anthropic"
        ]
    
    def is_ai_related(self, article: Dict) -> bool:
        """Check if article is AI-related"""
        text = f"{article['title']} {article['description']}".lower()
        return any(keyword.lower() in text for keyword in self.ai_keywords)
    
    def run_aggregation(self):
        """Run the complete aggregation pipeline"""
        logger.info("Starting AI news aggregation...")
        
        all_articles = []
        
        # Fetch from RSS feeds
        for feed_url in self.rss_feeds:
            articles = self.rss_parser.parse_feed(feed_url)
            all_articles.extend(articles)
        
        # Filter AI-related articles
        ai_articles = [a for a in all_articles if self.is_ai_related(a)]
        logger.info(f"Found {len(ai_articles)} AI articles out of {len(all_articles)} total")
        
        # Remove duplicates
        seen_titles = set()
        unique_articles = []
        for article in ai_articles:
            if article['title'] not in seen_titles:
                seen_titles.add(article['title'])
                unique_articles.append(article)
        
        # Add summaries
        for article in unique_articles:
            summary = self.summarizer.summarize_text(article['description'])
            article['summary'] = summary
        
        # Create overall summary
        overall_summary = self.summarizer.create_overall_summary(unique_articles)
        
        # Generate outputs
        self.output_generator.generate_json_output(unique_articles, overall_summary)
        self.output_generator.generate_html_output(unique_articles, overall_summary)
        
        return unique_articles, overall_summary


def main():
    """Main function"""
    args = sys.argv[1:]
    verbose = '--verbose' in args or '-v' in args
    
    if '--help' in args or '-h' in args:
        print("""
BBC News AI Aggregator - Standalone Version

Usage: python standalone_main.py [options]

Options:
    --verbose, -v    Enable verbose logging
    --help, -h       Show this help
        """)
        return 0
    
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    print("=" * 60)
    print("BBC NEWS AI AGGREGATOR (STANDALONE)")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        aggregator = StandaloneAINewsAggregator()
        articles, summary = aggregator.run_aggregation()
        
        print(f"\nRESULTS:")
        print(f"Found {len(articles)} AI-related articles")
        print(f"\nOverall Summary:")
        print(summary)
        
        print(f"\nArticles:")
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article['title']}")
        
        print(f"\nOutput files generated in 'output/' directory")
        print("=" * 60)
        
        return 0
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
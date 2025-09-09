#!/usr/bin/env python3
"""
BBC News AI Aggregator - Simplified Version

This simplified version works with minimal dependencies,
using basic text processing instead of advanced ML models.

Usage:
    python simple_main.py [--today-only] [--extract-content] [--verbose]
"""

import sys
import os
import json
import logging
from datetime import datetime
from urllib.parse import urlparse

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from news_fetcher import BBCNewsFetcher
from simple_extractor import SimpleContentExtractor
from simple_summarizer import SimpleSummarizer
from output_generator import OutputGenerator

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SimpleAINewsAggregator:
    """Simplified AI news aggregator with minimal dependencies"""
    
    def __init__(self):
        self.news_fetcher = None
        self.content_extractor = None
        self.summarizer = None
        self.output_generator = None
        
    def initialize_components(self):
        """Initialize all components"""
        logger.info("Initializing Simple AI News Aggregator components...")
        
        try:
            self.news_fetcher = BBCNewsFetcher()
            self.content_extractor = SimpleContentExtractor()
            self.summarizer = SimpleSummarizer()
            self.output_generator = OutputGenerator()
            
            logger.info("All components initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            return False
    
    def run_aggregation(self, today_only: bool = True, extract_full_content: bool = False):
        """
        Run the simplified news aggregation pipeline
        
        Args:
            today_only: Whether to fetch only today's news
            extract_full_content: Whether to extract full article content (slower)
        """
        logger.info("Starting simplified AI news aggregation pipeline...")
        
        try:
            # Step 1: Fetch AI-related news from BBC RSS feeds
            logger.info("Step 1: Fetching AI news from BBC RSS feeds...")
            articles = self.news_fetcher.fetch_ai_news(today_only=today_only)
            
            if not articles:
                logger.warning("No AI-related articles found")
                return [], "No AI news found for the specified period."
            
            logger.info(f"Found {len(articles)} AI-related articles")
            
            # Step 2: Extract full content (optional and slower)
            if extract_full_content:
                logger.info("Step 2: Extracting full article content...")
                articles = self.content_extractor.extract_multiple(articles)
                logger.info(f"Content extracted from articles")
            
            # Step 3: Summarize articles using simple text processing
            logger.info("Step 3: Summarizing articles with basic text processing...")
            articles = self.summarizer.summarize_articles(articles)
            
            # Step 4: Create overall summary
            logger.info("Step 4: Creating overall summary...")
            overall_summary = self.summarizer.create_overall_summary(articles)
            
            # Step 5: Generate output files
            logger.info("Step 5: Generating output files...")
            output_files = self.output_generator.generate_outputs(articles, overall_summary)
            
            logger.info("AI news aggregation completed successfully!")
            logger.info(f"Generated output files: {output_files}")
            
            return articles, overall_summary
            
        except Exception as e:
            logger.error(f"Error during news aggregation: {e}")
            raise e


def print_help():
    """Print usage help"""
    print("""
BBC News AI Aggregator - Simplified Version

Usage:
    python simple_main.py [options]

Options:
    --today-only        Fetch only today's news (default)
    --all-recent        Fetch all recent news from RSS feeds
    --extract-content   Extract full article content (slower)
    --rss-only          Use only RSS descriptions (faster, default)
    --verbose          Enable verbose logging
    --help             Show this help message

Examples:
    python simple_main.py
    python simple_main.py --all-recent --extract-content --verbose
    """)


def main():
    """Main function"""
    import argparse
    
    # Parse command line arguments
    args = sys.argv[1:]
    
    today_only = True
    extract_content = False
    verbose = False
    
    if '--help' in args or '-h' in args:
        print_help()
        return 0
    
    if '--all-recent' in args:
        today_only = False
    
    if '--extract-content' in args:
        extract_content = True
    
    if '--verbose' in args or '-v' in args:
        verbose = True
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("=" * 60)
    logger.info("BBC NEWS AI AGGREGATOR (SIMPLIFIED VERSION)")
    logger.info("=" * 60)
    logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Configuration: today_only={today_only}, extract_content={extract_content}")
    
    try:
        # Initialize the aggregator
        aggregator = SimpleAINewsAggregator()
        
        # Initialize components
        if not aggregator.initialize_components():
            logger.error("Failed to initialize components. Exiting.")
            return 1
        
        # Run the aggregation
        articles, overall_summary = aggregator.run_aggregation(
            today_only=today_only,
            extract_full_content=extract_content
        )
        
        # Display results
        print("\n" + "=" * 60)
        print("AGGREGATION RESULTS")
        print("=" * 60)
        print(f"Total articles processed: {len(articles)}")
        print(f"\nOverall Summary:")
        print("-" * 20)
        print(overall_summary)
        
        if articles:
            print(f"\nArticle Titles:")
            print("-" * 20)
            for i, article in enumerate(articles, 1):
                title = article.get('title', 'Unknown title')
                print(f"{i}. {title}")
                if verbose:
                    summary = article.get('summary', article.get('description', ''))[:200]
                    print(f"   Summary: {summary}...")
                    print(f"   Link: {article.get('link', '')}")
                    print()
        
        print(f"\nOutput files generated in: output/")
        print("=" * 60)
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Application error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
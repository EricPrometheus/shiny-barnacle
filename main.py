#!/usr/bin/env python3
"""
BBC News AI Aggregator and Summarizer

This application fetches AI-related news from BBC News RSS feeds,
extracts full article content, summarizes each article, and generates
comprehensive reports in multiple formats.

Usage:
    python main.py [OPTIONS]

Example:
    python main.py --today-only --verbose
"""

import click
import logging
from datetime import datetime
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from news_fetcher import BBCNewsFetcher
from content_extractor import ArticleExtractor
from summarizer import NewsSummarizer
from output_generator import OutputGenerator

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AINewsAggregator:
    """Main application class for AI news aggregation"""
    
    def __init__(self):
        self.news_fetcher = None
        self.content_extractor = None
        self.summarizer = None
        self.output_generator = None
        
    def initialize_components(self):
        """Initialize all application components"""
        logger.info("Initializing AI News Aggregator components...")
        
        try:
            self.news_fetcher = BBCNewsFetcher()
            self.content_extractor = ArticleExtractor()
            self.output_generator = OutputGenerator()
            
            # Initialize summarizer (this may take time for model loading)
            logger.info("Loading summarization model (this may take a few minutes)...")
            self.summarizer = NewsSummarizer()
            
            logger.info("All components initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            return False
    
    def run_aggregation(self, today_only: bool = True, extract_full_content: bool = True):
        """
        Run the full news aggregation pipeline
        
        Args:
            today_only: Whether to fetch only today's news
            extract_full_content: Whether to extract full article content
        """
        logger.info("Starting AI news aggregation pipeline...")
        
        try:
            # Step 1: Fetch AI-related news from BBC RSS feeds
            logger.info("Step 1: Fetching AI news from BBC RSS feeds...")
            articles = self.news_fetcher.fetch_ai_news(today_only=today_only)
            
            if not articles:
                logger.warning("No AI-related articles found")
                return [], "No AI news found for the specified period."
            
            logger.info(f"Found {len(articles)} AI-related articles")
            
            # Step 2: Extract full content (optional)
            if extract_full_content:
                logger.info("Step 2: Extracting full article content...")
                articles = self.content_extractor.extract_multiple(articles)
                logger.info(f"Successfully extracted content from {len(articles)} articles")
            
            # Step 3: Summarize articles
            logger.info("Step 3: Summarizing articles...")
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


@click.command()
@click.option('--today-only/--all-recent', default=True, 
              help='Fetch only today\'s news (default) or all recent news')
@click.option('--extract-content/--rss-only', default=True,
              help='Extract full article content (default) or use RSS summary only')
@click.option('--verbose', '-v', is_flag=True, 
              help='Enable verbose logging')
@click.option('--output-dir', default='output',
              help='Output directory for generated files')
def main(today_only, extract_content, verbose, output_dir):
    """
    BBC News AI Aggregator and Summarizer
    
    Fetches AI-related news from BBC News, summarizes articles, and generates reports.
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('transformers').setLevel(logging.INFO)
    
    # Update output directory if specified
    if output_dir != 'output':
        import config
        config.OUTPUT_DIR = output_dir
    
    logger.info("=" * 60)
    logger.info("BBC NEWS AI AGGREGATOR AND SUMMARIZER")
    logger.info("=" * 60)
    logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Configuration: today_only={today_only}, extract_content={extract_content}")
    logger.info(f"Output directory: {output_dir}")
    
    try:
        # Initialize the aggregator
        aggregator = AINewsAggregator()
        
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
                print(f"{i}. {article.get('title', 'Unknown title')}")
        
        print(f"\nOutput files generated in: {output_dir}/")
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
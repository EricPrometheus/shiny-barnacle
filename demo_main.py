#!/usr/bin/env python3
"""
BBC News AI Aggregator - Demo Version with Mock Data

This version demonstrates the functionality with sample AI news data
when network access is not available.
"""

import sys
import os
import json
import logging
from datetime import datetime

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from standalone_main import StandaloneSummarizer, StandaloneOutputGenerator

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mock AI news data for demonstration
MOCK_AI_NEWS = [
    {
        "title": "AI revolutionizes medical diagnosis with 95% accuracy breakthrough",
        "description": "New artificial intelligence systems developed by UK researchers are helping doctors diagnose complex diseases with unprecedented accuracy. The machine learning algorithms can analyze medical scans and patient data to identify conditions that might be missed by human experts. Hospitals across Britain are beginning to implement these AI-powered diagnostic tools to improve patient outcomes and reduce waiting times. The technology represents a significant advancement in healthcare AI applications.",
        "link": "https://www.bbc.com/news/technology-ai-medical-diagnosis",
        "published": "Mon, 09 Sep 2024 08:30:00 GMT",
        "source": "BBC News"
    },
    {
        "title": "ChatGPT competitor launches with focus on business automation",
        "description": "A new AI language model designed specifically for business applications has been launched by a European startup. The system promises to automate routine tasks like email responses, report generation, and customer service inquiries. Early testing shows the AI can handle complex business scenarios while maintaining professional tone and accuracy. Companies are already integrating the technology to streamline their operations and reduce administrative workload.",
        "link": "https://www.bbc.com/news/business-ai-automation-chatgpt",
        "published": "Mon, 09 Sep 2024 07:15:00 GMT",
        "source": "BBC News"
    },
    {
        "title": "Google's DeepMind unveils breakthrough in protein structure prediction",
        "description": "Researchers at Google DeepMind have announced a major advancement in using artificial intelligence to predict protein structures. The new AI model can determine how proteins fold with remarkable precision, potentially accelerating drug discovery and medical research. Scientists believe this breakthrough could lead to new treatments for diseases like Alzheimer's and Parkinson's. The technology demonstrates AI's growing capability to solve complex scientific problems that have puzzled researchers for decades.",
        "link": "https://www.bbc.com/news/science-deepmind-protein-ai",
        "published": "Mon, 09 Sep 2024 06:45:00 GMT",
        "source": "BBC News"
    },
    {
        "title": "Autonomous vehicles tested in major UK cities with AI safety systems",
        "description": "Self-driving cars equipped with advanced artificial intelligence are being tested on public roads in London, Manchester, and Birmingham. The vehicles use machine learning algorithms to navigate complex urban environments while ensuring passenger safety. Transport officials say the AI systems can react faster than human drivers to potential hazards. The trials represent a significant step toward fully autonomous transportation in Britain.",
        "link": "https://www.bbc.com/news/transport-autonomous-vehicles-ai",
        "published": "Mon, 09 Sep 2024 05:20:00 GMT",
        "source": "BBC News"
    },
    {
        "title": "AI-powered robots begin work in UK manufacturing plants",
        "description": "Intelligent robotic systems are being deployed across British manufacturing facilities to increase efficiency and precision. These AI-driven machines can adapt to different production requirements and work alongside human employees safely. The robots use computer vision and machine learning to perform complex assembly tasks that previously required skilled workers. Industry experts predict this technology will transform UK manufacturing competitiveness on the global stage.",
        "link": "https://www.bbc.com/news/business-ai-robots-manufacturing",
        "published": "Mon, 09 Sep 2024 04:10:00 GMT",
        "source": "BBC News"
    }
]


class DemoAINewsAggregator:
    """Demo version of AI news aggregator with mock data"""
    
    def __init__(self):
        self.summarizer = StandaloneSummarizer()
        self.output_generator = StandaloneOutputGenerator()
    
    def run_demo_aggregation(self):
        """Run aggregation with mock data"""
        logger.info("Starting demo AI news aggregation with mock data...")
        
        articles = MOCK_AI_NEWS.copy()
        
        logger.info(f"Processing {len(articles)} sample AI articles")
        
        # Add summaries to each article
        for article in articles:
            summary = self.summarizer.summarize_text(article['description'])
            article['summary'] = summary
            logger.info(f"Summarized: {article['title'][:50]}...")
        
        # Create overall summary
        overall_summary = self.summarizer.create_overall_summary(articles)
        logger.info("Created overall summary")
        
        # Generate output files
        json_file = self.output_generator.generate_json_output(articles, overall_summary)
        html_file = self.output_generator.generate_html_output(articles, overall_summary)
        
        logger.info("Demo aggregation completed successfully!")
        
        return articles, overall_summary, [json_file, html_file]


def main():
    """Main demo function"""
    args = sys.argv[1:]
    verbose = '--verbose' in args or '-v' in args
    
    if '--help' in args or '-h' in args:
        print("""
BBC News AI Aggregator - Demo Version

This demo version shows how the aggregator works with sample AI news data.

Usage: python demo_main.py [options]

Options:
    --verbose, -v    Enable verbose logging
    --help, -h       Show this help
        """)
        return 0
    
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    print("=" * 70)
    print("BBC NEWS AI AGGREGATOR - DEMO VERSION")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Using sample AI news data for demonstration")
    print()
    
    try:
        aggregator = DemoAINewsAggregator()
        articles, overall_summary, output_files = aggregator.run_demo_aggregation()
        
        print("DEMO RESULTS:")
        print("=" * 70)
        print(f"📊 Total articles processed: {len(articles)}")
        print()
        print("📝 OVERALL SUMMARY:")
        print("-" * 40)
        print(overall_summary)
        print()
        
        print("📰 INDIVIDUAL ARTICLES:")
        print("-" * 40)
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article['title']}")
            if verbose:
                print(f"   Summary: {article['summary']}")
                print(f"   Link: {article['link']}")
                print(f"   Published: {article['published']}")
                print()
        
        print("\n📁 OUTPUT FILES:")
        print("-" * 40)
        for file_path in output_files:
            print(f"✅ Generated: {file_path}")
        
        print()
        print("🌐 You can open the HTML file in your browser to see the formatted report!")
        print("=" * 70)
        
        return 0
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Demo error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
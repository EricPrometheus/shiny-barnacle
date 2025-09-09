"""
Scheduler for daily news aggregation
"""

import schedule
import time
import logging
from datetime import datetime
from main import AINewsAggregator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def daily_news_job():
    """Job to run daily AI news aggregation"""
    logger.info("Starting scheduled daily AI news aggregation...")
    
    try:
        aggregator = AINewsAggregator()
        
        # Initialize components
        if aggregator.initialize_components():
            # Run aggregation for today's news only
            articles, overall_summary = aggregator.run_aggregation(
                today_only=True,
                extract_full_content=True
            )
            
            logger.info(f"Daily aggregation completed. Processed {len(articles)} articles.")
        else:
            logger.error("Failed to initialize components for scheduled job")
            
    except Exception as e:
        logger.error(f"Error in scheduled job: {e}")


def main():
    """Main scheduler function"""
    logger.info("Starting AI News Aggregator Scheduler")
    logger.info("Daily aggregation scheduled for 09:00")
    
    # Schedule daily job at 9 AM
    schedule.every().day.at("09:00").do(daily_news_job)
    
    # Also allow manual trigger every hour for testing
    # schedule.every().hour.do(daily_news_job)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.error(f"Scheduler error: {e}")


if __name__ == "__main__":
    main()
"""
Configuration settings for BBC News AI Aggregator
"""

# BBC News RSS feeds
BBC_TECH_RSS = "http://feeds.bbci.co.uk/news/technology/rss.xml"
BBC_BUSINESS_RSS = "http://feeds.bbci.co.uk/news/business/rss.xml"
BBC_WORLD_RSS = "http://feeds.bbci.co.uk/news/world/rss.xml"

# AI-related keywords to filter news
AI_KEYWORDS = [
    "artificial intelligence", "ai", "machine learning", "ml", "deep learning",
    "neural network", "chatgpt", "gpt", "openai", "google ai", "deepmind",
    "autonomous", "automation", "robot", "algorithm", "data science",
    "computer vision", "natural language", "nlp", "generative ai",
    "large language model", "llm", "transformer", "bert", "claude",
    "anthropic", "microsoft ai", "meta ai", "nvidia ai"
]

# Summarization settings
MAX_SUMMARY_LENGTH = 200
MIN_ARTICLE_LENGTH = 100

# Output settings
OUTPUT_DIR = "output"
JSON_OUTPUT = True
HTML_OUTPUT = True

# Request settings
REQUEST_TIMEOUT = 30
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
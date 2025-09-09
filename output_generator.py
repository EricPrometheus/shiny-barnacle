"""
Output generation module for creating formatted reports
"""

import json
import os
from datetime import datetime
from typing import List, Dict
import logging

from config import OUTPUT_DIR, JSON_OUTPUT, HTML_OUTPUT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OutputGenerator:
    """Generates formatted output files for the aggregated news"""
    
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"Created output directory: {self.output_dir}")
    
    def generate_json_output(self, articles: List[Dict], overall_summary: str) -> str:
        """Generate JSON output file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_news_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        output_data = {
            "generation_time": datetime.now().isoformat(),
            "total_articles": len(articles),
            "overall_summary": overall_summary,
            "articles": articles
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Generated JSON output: {filepath}")
        return filepath
    
    def generate_html_output(self, articles: List[Dict], overall_summary: str) -> str:
        """Generate HTML output file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_news_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        # Generate HTML content
        html_content = self._create_html_template(articles, overall_summary)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Generated HTML output: {filepath}")
        return filepath
    
    def _create_html_template(self, articles: List[Dict], overall_summary: str) -> str:
        """Create HTML template for the news report"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BBC AI News Summary - {today}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #bb1919;
            color: white;
            padding: 20px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .summary-box {{
            background-color: #e8f4f8;
            padding: 20px;
            border-left: 5px solid #007cba;
            margin-bottom: 30px;
        }}
        .article {{
            background-color: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .article-title {{
            color: #bb1919;
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .article-meta {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 15px;
        }}
        .article-summary {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        .article-link {{
            color: #007cba;
            text-decoration: none;
            font-weight: bold;
        }}
        .article-link:hover {{
            text-decoration: underline;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #666;
            font-size: 0.9em;
        }}
        .stats {{
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>BBC AI News Summary</h1>
        <p>Daily AI News Aggregation - {today}</p>
    </div>
    
    <div class="stats">
        <strong>📊 Statistics:</strong> Found {len(articles)} AI-related articles from BBC News
    </div>
    
    <div class="summary-box">
        <h2>🔍 Overall Summary</h2>
        <p>{overall_summary}</p>
    </div>
    
    <div class="articles">
        <h2>📰 Individual Articles</h2>
"""
        
        # Add individual articles
        for i, article in enumerate(articles, 1):
            published = article.get('published', 'Unknown date')
            title = article.get('title', 'No title')
            summary = article.get('summary', article.get('description', 'No summary available'))
            link = article.get('link', '#')
            authors = article.get('authors', [])
            author_str = ', '.join(authors) if authors else 'BBC News'
            
            html += f"""
        <div class="article">
            <div class="article-title">{i}. {title}</div>
            <div class="article-meta">
                👤 {author_str} | 📅 {published}
            </div>
            <div class="article-summary">
                {summary}
            </div>
            <a href="{link}" target="_blank" class="article-link">Read full article →</a>
        </div>
"""
        
        html += f"""
    </div>
    
    <div class="footer">
        <p>Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}</p>
        <p>Powered by BBC News AI Aggregator</p>
    </div>
</body>
</html>
"""
        
        return html
    
    def generate_text_output(self, articles: List[Dict], overall_summary: str) -> str:
        """Generate simple text output file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_news_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"BBC AI News Summary - {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"OVERALL SUMMARY ({len(articles)} articles):\n")
            f.write("-" * 40 + "\n")
            f.write(f"{overall_summary}\n\n")
            
            f.write("INDIVIDUAL ARTICLES:\n")
            f.write("-" * 40 + "\n\n")
            
            for i, article in enumerate(articles, 1):
                f.write(f"{i}. {article.get('title', 'No title')}\n")
                f.write(f"   Published: {article.get('published', 'Unknown')}\n")
                f.write(f"   Link: {article.get('link', 'N/A')}\n")
                f.write(f"   Summary: {article.get('summary', article.get('description', 'No summary'))}\n\n")
            
            f.write(f"\nGenerated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}\n")
        
        logger.info(f"Generated text output: {filepath}")
        return filepath
    
    def generate_outputs(self, articles: List[Dict], overall_summary: str) -> List[str]:
        """Generate all configured output formats"""
        generated_files = []
        
        if JSON_OUTPUT:
            json_file = self.generate_json_output(articles, overall_summary)
            generated_files.append(json_file)
        
        if HTML_OUTPUT:
            html_file = self.generate_html_output(articles, overall_summary)
            generated_files.append(html_file)
        
        # Always generate text output
        text_file = self.generate_text_output(articles, overall_summary)
        generated_files.append(text_file)
        
        logger.info(f"Generated {len(generated_files)} output files")
        return generated_files


if __name__ == "__main__":
    generator = OutputGenerator()
    
    # Test with sample data
    sample_articles = [
        {
            "title": "AI revolutionizes healthcare",
            "summary": "New AI systems are helping doctors diagnose diseases faster.",
            "link": "https://www.bbc.com/news/test1",
            "published": "Mon, 01 Jan 2024 12:00:00 GMT"
        }
    ]
    
    sample_summary = "AI continues to transform various industries with significant breakthroughs."
    
    files = generator.generate_outputs(sample_articles, sample_summary)
    for file in files:
        print(f"Generated: {file}")
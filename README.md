# BBC News AI Aggregator and Summarizer

这个项目能够从BBC新闻中聚合当日AI相关新闻并进行智能归纳总结。

A project that aggregates daily AI-related news from BBC News and provides intelligent summarization.

## Features 🚀

- **RSS Feed Monitoring**: Automatically monitors BBC News RSS feeds (Technology, Business, World)
- **AI Content Filtering**: Intelligently identifies AI-related articles using keyword matching
- **Content Extraction**: Extracts full article content from BBC News pages
- **Smart Summarization**: Uses transformer models to generate concise summaries
- **Multiple Output Formats**: Generates reports in JSON, HTML, and text formats
- **Daily Scheduling**: Can be configured to run automatically every day
- **Command Line Interface**: Easy-to-use CLI with various options

## 中文说明

本项目实现了以下功能：
- 自动从BBC新闻RSS订阅源获取新闻
- 智能筛选AI相关的新闻内容
- 提取完整文章内容
- 使用AI模型生成新闻摘要
- 生成多种格式的日报（JSON、HTML、文本）
- 支持定时任务，每日自动运行

## Installation 📦

1. Clone the repository:
```bash
git clone https://github.com/EricPrometheus/shiny-barnacle.git
cd shiny-barnacle
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download NLTK data (required for text processing):
```bash
python -c "import nltk; nltk.download('punkt')"
```

## Usage 💻

### Basic Usage

Run the aggregator to get today's AI news:
```bash
python main.py
```

### Command Line Options

```bash
# Get only today's news (default)
python main.py --today-only

# Get all recent news
python main.py --all-recent

# Extract full content from articles (default)
python main.py --extract-content

# Use only RSS summaries (faster)
python main.py --rss-only

# Enable verbose logging
python main.py --verbose

# Specify custom output directory
python main.py --output-dir /path/to/output

# Combine options
python main.py --today-only --extract-content --verbose
```

### Scheduled Daily Runs

To run the aggregator automatically every day at 9 AM:
```bash
python scheduler.py
```

## Output Files 📄

The application generates three types of output files in the `output/` directory:

1. **HTML Report** (`ai_news_YYYYMMDD_HHMMSS.html`): 
   - Beautiful, web-friendly format
   - Includes overall summary and individual article summaries
   - BBC-style formatting

2. **JSON Report** (`ai_news_YYYYMMDD_HHMMSS.json`):
   - Machine-readable format
   - Contains all metadata and summaries
   - Perfect for further processing

3. **Text Report** (`ai_news_YYYYMMDD_HHMMSS.txt`):
   - Simple plain text format
   - Easy to read in any text editor

## Configuration ⚙️

Key settings can be modified in `config.py`:

```python
# AI keywords for filtering
AI_KEYWORDS = ["artificial intelligence", "ai", "machine learning", ...]

# Summarization settings
MAX_SUMMARY_LENGTH = 200
MIN_ARTICLE_LENGTH = 100

# Output settings
OUTPUT_DIR = "output"
JSON_OUTPUT = True
HTML_OUTPUT = True
```

## Architecture 🏗️

The project consists of several modular components:

- `news_fetcher.py`: Fetches news from BBC RSS feeds and filters AI content
- `content_extractor.py`: Extracts full article content from URLs
- `summarizer.py`: Provides AI-powered summarization using transformer models
- `output_generator.py`: Generates formatted reports in multiple formats
- `main.py`: CLI interface and main application logic
- `scheduler.py`: Daily scheduling functionality
- `config.py`: Configuration settings

## Dependencies 📋

- `requests`: HTTP requests for fetching content
- `beautifulsoup4`: HTML parsing
- `feedparser`: RSS feed parsing
- `newspaper3k`: Article content extraction
- `transformers`: AI summarization models
- `torch`: PyTorch for transformer models
- `nltk`: Natural language processing utilities
- `schedule`: Task scheduling
- `click`: Command-line interface

## Example Output 📊

### HTML Report Preview
The HTML reports include:
- Overall summary of the day's AI news
- Individual article summaries
- Links to original BBC articles
- BBC-style formatting and colors
- Statistics and metadata

### Sample Text Output
```
BBC AI News Summary - 2024-01-15
============================================================

OVERALL SUMMARY (3 articles):
Today's AI developments focus on healthcare applications, with new 
diagnostic tools showing promising results. Companies are investing 
heavily in AI automation while addressing ethical concerns.

INDIVIDUAL ARTICLES:
----------------------------------------

1. AI revolutionizes medical diagnosis in UK hospitals
   Published: Mon, 15 Jan 2024 09:30:00 GMT
   Summary: New artificial intelligence systems are helping British 
   doctors diagnose diseases with 95% accuracy...
```

## Troubleshooting 🔧

### Common Issues

1. **Model Loading Errors**: 
   - The app will automatically fall back to a smaller model if the main one fails
   - Ensure you have sufficient disk space (models can be large)

2. **Network Timeouts**:
   - Check your internet connection
   - BBC RSS feeds might be temporarily unavailable

3. **No Articles Found**:
   - This might happen on days with limited AI news
   - Try using `--all-recent` to get older articles

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📜

This project is licensed under the MIT License.

## Disclaimer ⚠️

This tool is for educational and research purposes. Please respect BBC's terms of service and rate limits when using this application.

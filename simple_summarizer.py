"""
Simplified summarizer using basic text processing
(fallback for when transformer models are not available)
"""

import re
import logging
from typing import List, Dict
from collections import Counter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleSummarizer:
    """Basic text summarization using sentence scoring"""
    
    def __init__(self):
        # Common stop words for English
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'would', 'i', 'you', 'we', 'they',
            'this', 'these', 'those', 'what', 'where', 'when', 'who', 'why',
            'how', 'said', 'says', 'can', 'could', 'should', 'may', 'might'
        }
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Clean and tokenize text
        text = re.sub(r'[^\w\s]', '', text.lower())
        words = text.split()
        
        # Filter out stop words and short words
        keywords = [word for word in words 
                   if word not in self.stop_words and len(word) > 3]
        
        # Get most common words
        word_counts = Counter(keywords)
        return [word for word, count in word_counts.most_common(10)]
    
    def score_sentences(self, text: str, keywords: List[str]) -> List[tuple]:
        """Score sentences based on keyword frequency"""
        sentences = re.split(r'[.!?]+', text)
        scored_sentences = []
        
        for i, sentence in enumerate(sentences):
            if len(sentence.strip()) < 20:  # Skip very short sentences
                continue
                
            sentence_lower = sentence.lower()
            score = 0
            
            # Score based on keyword presence
            for keyword in keywords:
                score += sentence_lower.count(keyword.lower())
            
            # Bonus for sentences with AI-related terms
            ai_terms = ['ai', 'artificial intelligence', 'machine learning', 
                       'algorithm', 'technology', 'data', 'system']
            for term in ai_terms:
                if term in sentence_lower:
                    score += 2
            
            # Bonus for sentences at the beginning (often important)
            if i < 3:
                score += 1
            
            scored_sentences.append((sentence.strip(), score, i))
        
        # Sort by score (descending)
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        return scored_sentences
    
    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """Summarize text by selecting top-scored sentences"""
        if not text or len(text.strip()) < 100:
            return text
        
        # Extract keywords
        keywords = self.extract_keywords(text)
        
        # Score sentences
        scored_sentences = self.score_sentences(text, keywords)
        
        # Select top sentences (maintaining original order)
        selected_sentences = scored_sentences[:max_sentences]
        selected_sentences.sort(key=lambda x: x[2])  # Sort by original position
        
        # Join sentences
        summary = '. '.join([sent[0] for sent in selected_sentences])
        summary = summary.replace('..', '.').strip()
        
        # Ensure it ends with proper punctuation
        if summary and not summary.endswith(('.', '!', '?')):
            summary += '.'
        
        return summary
    
    def summarize_articles(self, articles: List[Dict]) -> List[Dict]:
        """Summarize multiple articles"""
        summarized_articles = []
        
        for i, article in enumerate(articles):
            logger.info(f"Summarizing article {i+1}/{len(articles)}: {article.get('title', 'Unknown')}")
            
            # Use full text if available, otherwise use description
            text = article.get('text', article.get('description', ''))
            
            if text:
                summary = self.summarize_text(text)
                article['summary'] = summary
            else:
                article['summary'] = article.get('description', 'No summary available')
            
            summarized_articles.append(article)
        
        logger.info(f"Summarized {len(summarized_articles)} articles")
        return summarized_articles
    
    def create_overall_summary(self, articles: List[Dict]) -> str:
        """Create an overall summary of all AI news"""
        if not articles:
            return "No AI news found for today."
        
        # Collect all titles and summaries
        all_text = " ".join([
            f"{article.get('title', '')} {article.get('summary', article.get('description', ''))}"
            for article in articles
        ])
        
        # Extract main themes
        keywords = self.extract_keywords(all_text)
        
        # Count topics
        topic_counts = {}
        for article in articles:
            title_text = f"{article.get('title', '')} {article.get('description', '')}".lower()
            
            # Categorize by topic
            if any(word in title_text for word in ['healthcare', 'medical', 'health', 'hospital']):
                topic_counts['healthcare'] = topic_counts.get('healthcare', 0) + 1
            elif any(word in title_text for word in ['business', 'company', 'investment', 'market']):
                topic_counts['business'] = topic_counts.get('business', 0) + 1
            elif any(word in title_text for word in ['chatgpt', 'gpt', 'openai', 'language model']):
                topic_counts['language_models'] = topic_counts.get('language_models', 0) + 1
            elif any(word in title_text for word in ['robot', 'autonomous', 'automation']):
                topic_counts['robotics'] = topic_counts.get('robotics', 0) + 1
            else:
                topic_counts['general_ai'] = topic_counts.get('general_ai', 0) + 1
        
        # Create summary
        summary_parts = [f"Today's AI news covers {len(articles)} articles"]
        
        if topic_counts:
            main_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            topic_desc = []
            for topic, count in main_topics:
                topic_name = topic.replace('_', ' ').title()
                topic_desc.append(f"{topic_name} ({count})")
            summary_parts.append(f"focusing on: {', '.join(topic_desc)}")
        
        # Add key themes
        if keywords:
            key_themes = ', '.join(keywords[:5])
            summary_parts.append(f"Key themes include: {key_themes}")
        
        summary = ". ".join(summary_parts) + "."
        
        return summary


if __name__ == "__main__":
    summarizer = SimpleSummarizer()
    
    test_text = """
    Artificial intelligence is rapidly transforming healthcare systems worldwide. 
    Doctors are now using AI-powered diagnostic tools to detect diseases earlier and more accurately. 
    Machine learning algorithms analyze medical images to identify cancerous cells that human eyes might miss. 
    These technological advances are improving patient outcomes and reducing healthcare costs. 
    However, experts warn about the need for proper regulation and training. 
    The integration of AI in hospitals requires careful planning and investment in infrastructure.
    """
    
    summary = summarizer.summarize_text(test_text)
    print(f"Original: {len(test_text)} characters")
    print(f"Summary: {len(summary)} characters") 
    print(f"Summary: {summary}")
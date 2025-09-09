"""
News summarization module using transformer models
"""

import logging
from typing import List, Dict
from transformers import pipeline, AutoTokenizer
import torch
from config import MAX_SUMMARY_LENGTH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsSummarizer:
    """Summarizes news articles using transformer models"""
    
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """
        Initialize the summarizer with a pre-trained model
        
        Args:
            model_name: Hugging Face model name for summarization
        """
        self.model_name = model_name
        self.summarizer = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load the summarization model"""
        try:
            logger.info(f"Loading summarization model: {self.model_name}")
            
            # Check if CUDA is available
            device = 0 if torch.cuda.is_available() else -1
            logger.info(f"Using device: {'GPU' if device == 0 else 'CPU'}")
            
            # Load summarization pipeline
            self.summarizer = pipeline(
                "summarization",
                model=self.model_name,
                device=device
            )
            
            # Load tokenizer for text length checking
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            # Fallback to a smaller model if the main one fails
            try:
                logger.info("Attempting to load fallback model: sshleifer/distilbart-cnn-12-6")
                self.model_name = "sshleifer/distilbart-cnn-12-6"
                device = 0 if torch.cuda.is_available() else -1
                self.summarizer = pipeline(
                    "summarization",
                    model=self.model_name,
                    device=device
                )
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                logger.info("Fallback model loaded successfully")
            except Exception as e2:
                logger.error(f"Error loading fallback model: {e2}")
                raise e2
    
    def _chunk_text(self, text: str, max_length: int = 1024) -> List[str]:
        """Split text into chunks that fit the model's input limit"""
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        for i in range(0, len(tokens), max_length):
            chunk_tokens = tokens[i:i + max_length]
            chunk_text = self.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
            chunks.append(chunk_text)
        
        return chunks
    
    def summarize_text(self, text: str, max_length: int = None) -> str:
        """
        Summarize a single text
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
            
        Returns:
            Summarized text
        """
        if not self.summarizer:
            return "Summarization model not available"
        
        if not text or len(text.strip()) < 50:
            return text  # Return original if too short
        
        try:
            max_len = max_length or MAX_SUMMARY_LENGTH
            min_len = min(50, max_len // 2)
            
            # Handle long texts by chunking
            chunks = self._chunk_text(text)
            summaries = []
            
            for chunk in chunks:
                summary = self.summarizer(
                    chunk,
                    max_length=max_len,
                    min_length=min_len,
                    do_sample=False
                )
                summaries.append(summary[0]['summary_text'])
            
            # If we have multiple chunks, summarize the combined summaries
            if len(summaries) > 1:
                combined_summary = " ".join(summaries)
                if len(self.tokenizer.encode(combined_summary)) > 1024:
                    final_summary = self.summarizer(
                        combined_summary,
                        max_length=max_len,
                        min_length=min_len,
                        do_sample=False
                    )
                    return final_summary[0]['summary_text']
                else:
                    return combined_summary
            else:
                return summaries[0]
                
        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            # Return first few sentences as fallback
            sentences = text.split('. ')
            return '. '.join(sentences[:3]) + '.'
    
    def summarize_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Summarize multiple articles
        
        Args:
            articles: List of article dictionaries with 'text' field
            
        Returns:
            List of articles with 'summary' field added
        """
        summarized_articles = []
        
        for i, article in enumerate(articles):
            logger.info(f"Summarizing article {i+1}/{len(articles)}: {article.get('title', 'Unknown')}")
            
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
        """
        Create an overall summary of all AI news for the day
        
        Args:
            articles: List of summarized articles
            
        Returns:
            Overall summary text
        """
        if not articles:
            return "No AI news found for today."
        
        # Combine all individual summaries
        combined_text = " ".join([
            f"{article.get('title', 'Unknown')}: {article.get('summary', '')}"
            for article in articles
        ])
        
        # Create an overall summary
        overall_summary = self.summarize_text(combined_text, max_length=300)
        
        return f"Today's AI News Summary ({len(articles)} articles): {overall_summary}"


if __name__ == "__main__":
    summarizer = NewsSummarizer()
    test_text = """
    Artificial intelligence is rapidly transforming various industries across the globe. 
    Companies are investing heavily in machine learning technologies to improve their operations 
    and customer experiences. Recent developments in large language models have shown 
    remarkable capabilities in natural language processing and generation. However, there 
    are also concerns about the ethical implications and potential job displacement caused 
    by AI automation. Researchers and policymakers are working together to establish 
    guidelines for responsible AI development and deployment.
    """
    
    summary = summarizer.summarize_text(test_text)
    print(f"Original text length: {len(test_text)} characters")
    print(f"Summary length: {len(summary)} characters")
    print(f"Summary: {summary}")
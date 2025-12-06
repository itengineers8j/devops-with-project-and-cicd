"""
Sentiment Analysis module for YouTube transcripts
"""
import re
from typing import Dict, List, Tuple
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download required NLTK resources
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

class SentimentAnalyzer:
    """Class to analyze sentiment in text"""
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
    
    def clean_transcript(self, transcript: str) -> str:
        """Remove timestamps and clean the transcript text"""
        # Remove timestamps like [00:00]
        cleaned_text = re.sub(r'\[\d+:\d+\]', '', transcript)
        # Remove extra whitespace
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        return cleaned_text
    
    def split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences using regex instead of NLTK tokenizer"""
        # Simple regex-based sentence splitting - more aggressive to get shorter quotes
        sentences = []
        # First split by obvious sentence boundaries
        raw_splits = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
        
        # Then further split long sentences by common conjunctions and pauses
        for raw in raw_splits:
            if len(raw.strip()) > 100:  # Only split long sentences
                sub_sentences = re.split(r'(?<=\,|\;)\s+|(?<=\sand\s)|(?<=\sbut\s)|(?<=\sor\s)|(?<=\sso\s)', raw)
                sentences.extend([s.strip() for s in sub_sentences if len(s.strip()) > 20])
            else:
                sentences.append(raw.strip())
                
        # Filter out very short sentences (likely not meaningful)
        return [s for s in sentences if len(s.strip()) > 20 and len(s.strip()) < 200]
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of a text segment"""
        return self.sia.polarity_scores(text)
    
    def get_top_quotes(self, transcript: str, top_n: int = 5, sentiment_type: str = 'positive') -> List[Dict]:
        """
        Extract top positive or negative quotes from transcript
        
        Args:
            transcript: The transcript text with timestamps
            top_n: Number of top sentences to return
            sentiment_type: 'positive' or 'negative'
            
        Returns:
            List of top quotes with their sentiment scores
        """
        # Clean and prepare text
        cleaned_text = self.clean_transcript(transcript)
        sentences = self.split_into_sentences(cleaned_text)
        
        # Analyze each sentence
        analyzed_sentences = []
        for sentence in sentences:
            sentiment = self.analyze_sentiment(sentence)
            analyzed_sentences.append({
                'text': sentence,
                'compound': sentiment['compound'],
                'positive': sentiment['pos'],
                'negative': sentiment['neg'],
                'neutral': sentiment['neu']
            })
        
        # Sort by compound score (overall sentiment)
        if sentiment_type == 'positive':
            filtered_sentences = sorted(
                [s for s in analyzed_sentences if s['compound'] > 0.2],  # Lower threshold to get more results
                key=lambda x: x['compound'],
                reverse=True
            )
        else:  # negative
            filtered_sentences = sorted(
                [s for s in analyzed_sentences if s['compound'] < -0.2],  # Lower threshold to get more results
                key=lambda x: x['compound']
            )
        
        # Format results - return just the quotes with scores
        top_quotes = [{'quote': self.format_quote(s['text']), 'score': s['compound']} 
                      for s in filtered_sentences[:top_n]]
        
        return top_quotes
    
    def format_quote(self, text: str) -> str:
        """Format a quote for better readability"""
        # Trim to reasonable length if too long
        if len(text) > 200:
            text = text[:197] + "..."
        
        # Clean up any remaining issues
        text = text.replace("  ", " ").strip()
        
        return f'"{text}"'

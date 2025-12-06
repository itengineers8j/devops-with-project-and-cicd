"""
Web Content Extraction Service
Handles the extraction of text content from web pages, blogs, and articles
"""
import re
import requests
from typing import Dict, Optional
from bs4 import BeautifulSoup
from newspaper import Article
import trafilatura
from urllib.parse import urlparse


class WebContentService:
    """Service for extracting and processing text content from web pages"""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        Check if a URL is valid
        
        Args:
            url: URL to check
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def extract_domain(url: str) -> str:
        """
        Extract domain name from URL
        
        Args:
            url: URL to extract domain from
            
        Returns:
            str: Domain name
        """
        try:
            parsed_uri = urlparse(url)
            domain = '{uri.netloc}'.format(uri=parsed_uri)
            return domain
        except Exception:
            return "unknown"
    
    @staticmethod
    def get_content_type(url: str, headers: Dict = None) -> Optional[str]:
        """
        Get content type of URL
        
        Args:
            url: URL to check
            headers: Optional request headers
            
        Returns:
            str: Content type or None if request fails
        """
        if not headers:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
        try:
            response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
            return response.headers.get('Content-Type', '')
        except Exception:
            return None
    
    @staticmethod
    def extract_with_newspaper(url: str) -> Dict:
        """
        Extract content using newspaper3k library
        
        Args:
            url: URL to extract content from
            
        Returns:
            Dict: Extracted content and metadata
        """
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()  # Run NLP to extract keywords and summary
            
            return {
                "status": "success",
                "title": article.title,
                "text": article.text,
                "summary": article.summary,
                "keywords": article.keywords,
                "authors": article.authors,
                "publish_date": article.publish_date.isoformat() if article.publish_date else None,
                "top_image": article.top_image,
                "method": "newspaper3k"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error extracting with newspaper3k: {str(e)}",
                "method": "newspaper3k"
            }
    
    @staticmethod
    def extract_with_trafilatura(url: str) -> Dict:
        """
        Extract content using trafilatura library
        
        Args:
            url: URL to extract content from
            
        Returns:
            Dict: Extracted content
        """
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded is None:
                return {
                    "status": "error",
                    "message": "Failed to download content",
                    "method": "trafilatura"
                }
                
            result = trafilatura.extract(downloaded, include_comments=False, 
                                        include_tables=True, output_format='text',
                                        with_metadata=True)
            
            if result is None:
                return {
                    "status": "error",
                    "message": "Failed to extract content",
                    "method": "trafilatura"
                }
                
            metadata = trafilatura.extract_metadata(downloaded)
            
            return {
                "status": "success",
                "title": metadata.title if metadata else None,
                "text": result,
                "authors": metadata.author if metadata else None,
                "publish_date": metadata.date if metadata else None,
                "method": "trafilatura"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error extracting with trafilatura: {str(e)}",
                "method": "trafilatura"
            }
    
    @staticmethod
    def extract_with_beautifulsoup(url: str) -> Dict:
        """
        Extract content using BeautifulSoup
        
        Args:
            url: URL to extract content from
            
        Returns:
            Dict: Extracted content
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script_or_style in soup(['script', 'style', 'header', 'footer', 'nav']):
                script_or_style.decompose()
                
            # Extract title
            title = soup.title.string if soup.title else None
            
            # Extract text from paragraphs
            paragraphs = soup.find_all('p')
            text = '\n\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            
            # If text is too short, try getting all text
            if len(text) < 100:
                text = soup.get_text(separator='\n\n')
                # Clean up text
                text = re.sub(r'\n+', '\n\n', text)
                text = re.sub(r'\s+', ' ', text)
                
            return {
                "status": "success",
                "title": title,
                "text": text,
                "method": "beautifulsoup"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error extracting with BeautifulSoup: {str(e)}",
                "method": "beautifulsoup"
            }
    
    @staticmethod
    def extract_content(url: str) -> Dict:
        """
        Extract content from a web page using multiple methods
        
        Args:
            url: URL to extract content from
            
        Returns:
            Dict: Extracted content using the best available method
        """
        if not WebContentService.is_valid_url(url):
            return {
                "status": "error",
                "message": "Invalid URL format"
            }
            
        # Try with trafilatura first (usually best for articles)
        trafilatura_result = WebContentService.extract_with_trafilatura(url)
        if trafilatura_result["status"] == "success" and trafilatura_result.get("text") and len(trafilatura_result["text"]) > 200:
            return trafilatura_result
            
        # Try with newspaper3k next
        newspaper_result = WebContentService.extract_with_newspaper(url)
        if newspaper_result["status"] == "success" and newspaper_result.get("text") and len(newspaper_result["text"]) > 200:
            return newspaper_result
            
        # Fall back to BeautifulSoup
        bs_result = WebContentService.extract_with_beautifulsoup(url)
        if bs_result["status"] == "success" and bs_result.get("text"):
            return bs_result
            
        # If all methods failed, return the best result we have
        for result in [trafilatura_result, newspaper_result, bs_result]:
            if result["status"] == "success" and result.get("text"):
                return result
                
        # If everything failed, return error
        return {
            "status": "error",
            "message": "Failed to extract content from the URL using all available methods"
        }

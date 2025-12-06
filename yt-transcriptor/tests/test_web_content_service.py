"""
Tests for the WebContentService class
"""
import pytest
from unittest.mock import patch, MagicMock
from app.web_content_service import WebContentService


class TestWebContentService:
    """Test cases for WebContentService"""
    
    def test_is_valid_url_valid(self):
        """Test valid URL validation"""
        assert WebContentService.is_valid_url("https://example.com") is True
        assert WebContentService.is_valid_url("http://example.com/path") is True
        
    def test_is_valid_url_invalid(self):
        """Test invalid URL validation"""
        assert WebContentService.is_valid_url("example.com") is False
        assert WebContentService.is_valid_url("not a url") is False
        
    def test_extract_domain(self):
        """Test domain extraction"""
        assert WebContentService.extract_domain("https://example.com/path") == "example.com"
        assert WebContentService.extract_domain("http://sub.example.com") == "sub.example.com"
        
    @patch('requests.head')
    def test_get_content_type(self, mock_head):
        """Test content type detection"""
        mock_response = MagicMock()
        mock_response.headers = {'Content-Type': 'text/html'}
        mock_head.return_value = mock_response
        
        content_type = WebContentService.get_content_type("https://example.com")
        assert content_type == 'text/html'
        
    @patch('app.web_content_service.WebContentService.extract_with_trafilatura')
    @patch('app.web_content_service.WebContentService.extract_with_newspaper')
    @patch('app.web_content_service.WebContentService.extract_with_beautifulsoup')
    def test_extract_content_trafilatura_success(self, mock_bs, mock_newspaper, mock_trafilatura):
        """Test content extraction with trafilatura success"""
        mock_trafilatura.return_value = {
            "status": "success",
            "title": "Test Title",
            "text": "This is a test content with more than 200 characters. " * 10,
            "method": "trafilatura"
        }
        
        result = WebContentService.extract_content("https://example.com")
        assert result["status"] == "success"
        assert result["method"] == "trafilatura"
        assert mock_newspaper.call_count == 0
        assert mock_bs.call_count == 0
        
    @patch('app.web_content_service.WebContentService.extract_with_trafilatura')
    @patch('app.web_content_service.WebContentService.extract_with_newspaper')
    @patch('app.web_content_service.WebContentService.extract_with_beautifulsoup')
    def test_extract_content_fallback(self, mock_bs, mock_newspaper, mock_trafilatura):
        """Test content extraction fallback"""
        mock_trafilatura.return_value = {
            "status": "error",
            "message": "Failed to extract",
            "method": "trafilatura"
        }
        
        mock_newspaper.return_value = {
            "status": "success",
            "title": "Test Title",
            "text": "This is a test content with more than 200 characters. " * 10,
            "method": "newspaper3k"
        }
        
        result = WebContentService.extract_content("https://example.com")
        assert result["status"] == "success"
        assert result["method"] == "newspaper3k"
        assert mock_bs.call_count == 0
        
    @patch('app.web_content_service.WebContentService.is_valid_url')
    def test_extract_content_invalid_url(self, mock_is_valid):
        """Test content extraction with invalid URL"""
        mock_is_valid.return_value = False
        
        result = WebContentService.extract_content("invalid-url")
        assert result["status"] == "error"
        assert "Invalid URL" in result["message"]

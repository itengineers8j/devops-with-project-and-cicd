"""
Tests for the API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.api import app


client = TestClient(app)


class TestAPI:
    """Test cases for API endpoints"""
    
    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "YouTube Transcript API" in response.json()["message"]
    
    @patch("app.transcript_service.TranscriptService.extract_video_id")
    @patch("app.transcript_service.TranscriptService.get_transcript")
    @patch("app.transcript_service.TranscriptService.format_transcript")
    def test_get_transcript_success(self, mock_format, mock_get, mock_extract):
        """Test successful transcript extraction"""
        # Mock the service methods
        mock_extract.return_value = "dQw4w9WgXcQ"
        mock_get.return_value = {
            "status": "success",
            "transcript": [{"text": "Test", "start": 0.0}],
            "language": "en"
        }
        mock_format.return_value = "[00:00] Test\n"
        
        # Make the request
        response = client.post(
            "/transcript",
            json={
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "format_text": True
            }
        )
        
        # Check the response
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["video_id"] == "dQw4w9WgXcQ"
        assert data["transcript"] == "[00:00] Test\n"
    
    @patch("app.transcript_service.TranscriptService.extract_video_id")
    def test_invalid_url(self, mock_extract):
        """Test handling of invalid URL"""
        mock_extract.return_value = None
        
        response = client.post(
            "/transcript",
            json={
                "url": "https://example.com",
                "format_text": True
            }
        )
        
        assert response.status_code == 400
        assert "Invalid YouTube URL" in response.json()["detail"]
    
    @patch("app.transcript_service.TranscriptService.extract_video_id")
    @patch("app.transcript_service.TranscriptService.get_transcript")
    def test_transcript_error(self, mock_get, mock_extract):
        """Test handling of transcript error"""
        mock_extract.return_value = "dQw4w9WgXcQ"
        mock_get.return_value = {
            "status": "error",
            "message": "Transcripts are disabled for this video"
        }
        
        response = client.post(
            "/transcript",
            json={
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "format_text": True
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "error"
        assert "Transcripts are disabled" in data["message"]

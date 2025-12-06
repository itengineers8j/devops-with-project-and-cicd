"""
Tests for the TranscriptService class
"""
import pytest
from app.transcript_service import TranscriptService


class TestTranscriptService:
    """Test cases for TranscriptService"""
    
    def test_extract_video_id_standard_url(self):
        """Test extracting video ID from standard YouTube URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        video_id = TranscriptService.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_short_url(self):
        """Test extracting video ID from short YouTube URL"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        video_id = TranscriptService.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_embed_url(self):
        """Test extracting video ID from embed YouTube URL"""
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        video_id = TranscriptService.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_invalid_url(self):
        """Test extracting video ID from invalid URL"""
        url = "https://example.com"
        video_id = TranscriptService.extract_video_id(url)
        assert video_id is None
    
    def test_format_transcript(self):
        """Test formatting transcript data"""
        transcript_data = [
            {"text": "Hello world", "start": 0.5},
            {"text": "This is a test", "start": 5.2},
            {"text": "Goodbye", "start": 10.0}
        ]
        
        formatted = TranscriptService.format_transcript(transcript_data)
        expected = "[00:00] Hello world\n[00:05] This is a test\n[00:10] Goodbye\n"
        
        assert formatted == expected

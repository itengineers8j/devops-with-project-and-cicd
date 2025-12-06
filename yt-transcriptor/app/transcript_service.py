"""
YouTube Transcript Service
Handles the extraction of transcripts from YouTube videos
"""
import re
from typing import Dict, List, Optional, Union

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound


class TranscriptService:
    """Service for extracting and processing YouTube video transcripts"""
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extract the YouTube video ID from a URL
        
        Args:
            url: YouTube video URL
            
        Returns:
            str: Video ID if found, None otherwise
        """
        # Regular expressions to match different YouTube URL formats
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  # Standard YouTube URLs
            r'(?:embed\/)([0-9A-Za-z_-]{11})',   # Embedded URLs
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'  # Short URLs
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    @staticmethod
    def get_transcript(video_id: str, language: Optional[str] = None) -> Dict[str, Union[str, List[Dict]]]:
        """
        Get transcript for a YouTube video
        
        Args:
            video_id: YouTube video ID
            language: Preferred language code (optional)
            
        Returns:
            Dict containing transcript data or error message
        """
        try:
            # Get available transcript languages
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # If language is specified, try to get that language
            if language:
                try:
                    transcript = transcript_list.find_transcript([language])
                    transcript_data = transcript.fetch()
                    return {
                        "status": "success",
                        "transcript": transcript_data,
                        "language": transcript.language_code
                    }
                except NoTranscriptFound:
                    # If specified language not found, fall back to default
                    pass
            
            # Get default transcript (usually auto-generated in video's language)
            transcript = transcript_list.find_transcript(['en'])  # Try English first
            transcript_data = transcript.fetch()
            
            return {
                "status": "success",
                "transcript": transcript_data,
                "language": transcript.language_code
            }
            
        except TranscriptsDisabled:
            return {
                "status": "error",
                "message": "Transcripts are disabled for this video"
            }
        except NoTranscriptFound:
            return {
                "status": "error",
                "message": "No transcript found for this video"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error retrieving transcript: {str(e)}"
            }
    
    @staticmethod
    def format_transcript(transcript_data: List[Dict]) -> str:
        """
        Format transcript data into readable text
        
        Args:
            transcript_data: List of transcript segments
            
        Returns:
            str: Formatted transcript text
        """
        formatted_text = ""
        
        for item in transcript_data:
            text = item.get('text', '')
            start_time = item.get('start', 0)
            
            # Format timestamp as MM:SS
            minutes = int(start_time // 60)
            seconds = int(start_time % 60)
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
            
            formatted_text += f"{timestamp} {text}\n"
        
        return formatted_text

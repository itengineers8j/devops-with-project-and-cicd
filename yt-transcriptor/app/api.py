"""
FastAPI application for content extraction (YouTube transcripts and web page content)
"""
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, HttpUrl, Field
from typing import Dict, List, Optional, Union, Any
import re

from app.transcript_service import TranscriptService
from app.web_content_service import WebContentService

# Initialize FastAPI app
app = FastAPI(
    title="Content Extraction API",
    description="API for extracting transcripts from YouTube videos and content from web pages",
    version="1.1.0"
)

# Define request and response models
class TranscriptRequest(BaseModel):
    url: HttpUrl
    language: Optional[str] = None
    format_text: bool = True

class TranscriptResponse(BaseModel):
    status: str
    video_id: Optional[str] = None
    language: Optional[str] = None
    transcript: Optional[Union[List[Dict], str]] = None
    message: Optional[str] = None

class WebContentRequest(BaseModel):
    url: HttpUrl

class WebContentResponse(BaseModel):
    status: str
    url: str
    title: Optional[str] = None
    text: Optional[str] = None
    summary: Optional[str] = None
    keywords: Optional[List[str]] = None
    authors: Optional[Union[List[str], str]] = None
    publish_date: Optional[str] = None
    top_image: Optional[str] = None
    method: Optional[str] = None
    message: Optional[str] = None

class ContentRequest(BaseModel):
    url: HttpUrl
    language: Optional[str] = None
    format_text: bool = Field(default=True, description="Format transcript text (for YouTube only)")

class ContentResponse(BaseModel):
    status: str
    url: str
    content_type: str
    title: Optional[str] = None
    text: Optional[str] = None
    video_id: Optional[str] = None
    language: Optional[str] = None
    summary: Optional[str] = None
    keywords: Optional[List[str]] = None
    authors: Optional[Union[List[str], str]] = None
    publish_date: Optional[str] = None
    top_image: Optional[str] = None
    method: Optional[str] = None
    message: Optional[str] = None

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Content Extraction API",
        "version": "1.1.0",
        "endpoints": {
            "/transcript": "Extract transcript from YouTube video URL",
            "/webpage": "Extract content from web page URL",
            "/content": "Universal endpoint - automatically detects content type"
        }
    }

@app.post("/transcript", response_model=TranscriptResponse, tags=["YouTube"])
async def get_transcript(request: TranscriptRequest):
    """
    Extract transcript from a YouTube video
    
    - **url**: YouTube video URL
    - **language**: Optional language code (e.g., 'en', 'es', 'fr')
    - **format_text**: Whether to return formatted text (default: True)
    """
    # Extract video ID from URL
    video_id = TranscriptService.extract_video_id(str(request.url))
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    # Get transcript
    result = TranscriptService.get_transcript(video_id, request.language)
    
    if result["status"] == "error":
        return {
            "status": "error",
            "message": result["message"],
            "video_id": video_id
        }
    
    # Format transcript if requested
    transcript_data = result["transcript"]
    if request.format_text:
        formatted_transcript = TranscriptService.format_transcript(transcript_data)
        transcript_output = formatted_transcript
    else:
        transcript_output = transcript_data
    
    return {
        "status": "success",
        "video_id": video_id,
        "language": result.get("language"),
        "transcript": transcript_output
    }

@app.get("/transcript", response_model=TranscriptResponse, tags=["YouTube"])
async def get_transcript_get(
    url: str = Query(..., description="YouTube video URL"),
    language: Optional[str] = Query(None, description="Language code (e.g., 'en', 'es')"),
    format_text: bool = Query(True, description="Whether to return formatted text")
):
    """
    Extract transcript from a YouTube video (GET method)
    
    - **url**: YouTube video URL
    - **language**: Optional language code (e.g., 'en', 'es', 'fr')
    - **format_text**: Whether to return formatted text (default: True)
    """
    # Create a request object and reuse the POST endpoint logic
    request = TranscriptRequest(url=url, language=language, format_text=format_text)
    return await get_transcript(request)

@app.post("/webpage", response_model=WebContentResponse, tags=["Web Content"])
async def get_webpage_content(request: WebContentRequest):
    """
    Extract content from a web page
    
    - **url**: Web page URL
    """
    # Extract content from web page
    result = WebContentService.extract_content(str(request.url))
    
    if result["status"] == "error":
        return {
            "status": "error",
            "url": str(request.url),
            "message": result["message"]
        }
    
    return {
        "status": "success",
        "url": str(request.url),
        **{k: v for k, v in result.items() if k != "status"}
    }

@app.get("/webpage", response_model=WebContentResponse, tags=["Web Content"])
async def get_webpage_content_get(
    url: str = Query(..., description="Web page URL")
):
    """
    Extract content from a web page (GET method)
    
    - **url**: Web page URL
    """
    # Create a request object and reuse the POST endpoint logic
    request = WebContentRequest(url=url)
    return await get_webpage_content(request)

@app.post("/content", response_model=ContentResponse, tags=["Universal"])
async def get_content(request: ContentRequest):
    """
    Universal endpoint - automatically detects content type and extracts accordingly
    
    - **url**: URL (YouTube video or web page)
    - **language**: Optional language code for YouTube transcripts
    - **format_text**: Whether to format transcript text (for YouTube only)
    """
    url = str(request.url)
    
    # Check if it's a YouTube URL
    video_id = TranscriptService.extract_video_id(url)
    
    if video_id:
        # It's a YouTube URL
        result = TranscriptService.get_transcript(video_id, request.language)
        
        if result["status"] == "error":
            return {
                "status": "error",
                "url": url,
                "content_type": "youtube",
                "video_id": video_id,
                "message": result["message"]
            }
        
        # Format transcript if requested
        transcript_data = result["transcript"]
        if request.format_text:
            text = TranscriptService.format_transcript(transcript_data)
        else:
            text = transcript_data
        
        return {
            "status": "success",
            "url": url,
            "content_type": "youtube",
            "video_id": video_id,
            "language": result.get("language"),
            "text": text
        }
    else:
        # It's a web page URL
        result = WebContentService.extract_content(url)
        
        if result["status"] == "error":
            return {
                "status": "error",
                "url": url,
                "content_type": "webpage",
                "message": result["message"]
            }
        
        return {
            "status": "success",
            "url": url,
            "content_type": "webpage",
            **{k: v for k, v in result.items() if k != "status"}
        }

@app.get("/content", response_model=ContentResponse, tags=["Universal"])
async def get_content_get(
    url: str = Query(..., description="URL (YouTube video or web page)"),
    language: Optional[str] = Query(None, description="Language code for YouTube transcripts"),
    format_text: bool = Query(True, description="Format transcript text (for YouTube only)")
):
    """
    Universal endpoint - automatically detects content type and extracts accordingly (GET method)
    
    - **url**: URL (YouTube video or web page)
    - **language**: Optional language code for YouTube transcripts
    - **format_text**: Whether to format transcript text (for YouTube only)
    """
    # Create a request object and reuse the POST endpoint logic
    request = ContentRequest(url=url, language=language, format_text=format_text)
    return await get_content(request)

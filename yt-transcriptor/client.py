"""
Command-line client for Content Extraction Tool
"""
import argparse
import json
import requests
import sys
import re


def extract_content(url, language=None, format_text=True, api_url="http://localhost:8000"):
    """
    Extract content from a URL (YouTube video or web page)
    
    Args:
        url: URL to extract content from
        language: Preferred language code (optional, for YouTube)
        format_text: Whether to return formatted text (for YouTube)
        api_url: API server URL
        
    Returns:
        Extracted content or error message
    """
    endpoint = f"{api_url}/content"
    
    try:
        response = requests.post(
            endpoint,
            json={
                "url": url,
                "language": language,
                "format_text": format_text
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                return data
            else:
                return f"Error: {data['message']}"
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.RequestException as e:
        return f"Connection error: {str(e)}"


def main():
    """Main function for CLI"""
    parser = argparse.ArgumentParser(description="Extract content from URLs (YouTube videos or web pages)")
    parser.add_argument("url", help="URL to extract content from")
    parser.add_argument("-l", "--language", help="Preferred language code for YouTube transcripts (e.g., 'en', 'es')")
    parser.add_argument("--raw", action="store_true", help="Output raw data (JSON)")
    parser.add_argument("--api", default="http://localhost:8000", help="API server URL")
    parser.add_argument("-o", "--output", help="Output file (default: print to stdout)")
    
    args = parser.parse_args()
    
    # Extract content
    result = extract_content(
        args.url,
        language=args.language,
        format_text=not args.raw,
        api_url=args.api
    )
    
    # Format output
    if isinstance(result, dict):
        if args.raw:
            output = json.dumps(result, indent=2)
        else:
            if result.get("content_type") == "youtube":
                output = result.get("text", "No transcript available")
            else:
                # Format web page content
                title = result.get("title", "No title")
                text = result.get("text", "No content available")
                
                output = f"Title: {title}\n\n{text}"
    else:
        output = result  # Error message
    
    # Output result
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Content saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()

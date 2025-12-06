#!/usr/bin/env python3
"""
Quote Extractor - Extract positive and negative quotes from YouTube videos or web pages
"""
import argparse
import json
import sys
import requests
from sentiment_analyzer import SentimentAnalyzer

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


def extract_quotes(transcript_text, top_n=5, sentiment_type='positive'):
    """
    Extract top positive or negative quotes from transcript text
    
    Args:
        transcript_text: Text to analyze
        top_n: Number of top quotes to return
        sentiment_type: 'positive' or 'negative'
        
    Returns:
        List of quotes with sentiment scores
    """
    analyzer = SentimentAnalyzer()
    quotes = analyzer.get_top_quotes(transcript_text, top_n, sentiment_type)
    
    return quotes


def format_quotes_output(quotes, sentiment_type='positive'):
    """Format quotes for display"""
    output = "\n" + "="*80 + "\n"
    output += f"TOP {len(quotes)} {sentiment_type.upper()} QUOTES\n"
    output += "="*80 + "\n\n"
    
    for i, item in enumerate(quotes, 1):
        output += f"{i}. {item['quote']} (Score: {item['score']:.3f})\n\n"
    
    return output


def main():
    """Main function for CLI"""
    parser = argparse.ArgumentParser(description="Extract positive or negative quotes from YouTube videos or web pages")
    parser.add_argument("url", help="URL to extract content from")
    parser.add_argument("-l", "--language", help="Preferred language code for YouTube transcripts (e.g., 'en', 'es')")
    parser.add_argument("--raw", action="store_true", help="Output raw data (JSON)")
    parser.add_argument("--api", default="http://localhost:8000", help="API server URL")
    parser.add_argument("-o", "--output", help="Output file (default: print to stdout)")
    parser.add_argument("--type", choices=['positive', 'negative'], default='positive', 
                        help="Type of quotes to extract (default: positive)")
    parser.add_argument("--top", type=int, default=5, help="Number of top quotes to show")
    parser.add_argument("--transcript-only", action="store_true", help="Output only the transcript without sentiment analysis")
    
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
        if result.get("content_type") == "youtube":
            transcript_text = result.get("text", "No transcript available")
            
            # If transcript-only flag is set, just output the transcript
            if args.transcript_only:
                output = transcript_text
                if args.raw:
                    output = json.dumps({"url": args.url, "transcript": transcript_text}, indent=2)
            elif transcript_text != "No transcript available":
                quotes = extract_quotes(transcript_text, args.top, args.type)
                
                if args.raw:
                    output = json.dumps({"url": args.url, "quotes": quotes}, indent=2)
                else:
                    output = format_quotes_output(quotes, args.type)
            else:
                output = "Error: No transcript available for this video"
        else:
            # Handle web page content
            title = result.get("title", "No title")
            text = result.get("text", "No content available")
            
            # If transcript-only flag is set, just output the text content
            if args.transcript_only:
                output = f"Title: {title}\n\n{text}"
                if args.raw:
                    output = json.dumps({"url": args.url, "title": title, "content": text}, indent=2)
            elif text != "No content available":
                quotes = extract_quotes(text, args.top, args.type)
                
                if args.raw:
                    output = json.dumps({"url": args.url, "title": title, "quotes": quotes}, indent=2)
                else:
                    output = f"Title: {title}\n\n"
                    output += format_quotes_output(quotes, args.type)
            else:
                output = "Error: No content available from this web page"
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

#!/usr/bin/env python3
"""
Enhanced client for Content Extraction Tool with sentiment analysis
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


def analyze_sentiment(transcript_text, top_n=5):
    """
    Analyze sentiment in transcript text
    
    Args:
        transcript_text: Text to analyze
        top_n: Number of top positive/negative sentences to return
        
    Returns:
        Dictionary with top positive and negative sentences
    """
    analyzer = SentimentAnalyzer()
    top_positive, top_negative = analyzer.get_top_sentiments(transcript_text, top_n)
    
    return {
        "top_positive": top_positive,
        "top_negative": top_negative
    }


def format_sentiment_results(sentiment_results):
    """Format sentiment analysis results for display"""
    output = "\n" + "="*80 + "\n"
    output += "SENTIMENT ANALYSIS RESULTS\n"
    output += "="*80 + "\n\n"
    
    output += "TOP POSITIVE STATEMENTS:\n"
    output += "-"*80 + "\n"
    for i, item in enumerate(sentiment_results["top_positive"], 1):
        output += f"{i}. \"{item['text']}\" (Score: {item['score']:.3f})\n\n"
    
    output += "\nTOP NEGATIVE STATEMENTS:\n"
    output += "-"*80 + "\n"
    for i, item in enumerate(sentiment_results["top_negative"], 1):
        output += f"{i}. \"{item['text']}\" (Score: {item['score']:.3f})\n\n"
    
    return output


def main():
    """Main function for CLI"""
    parser = argparse.ArgumentParser(description="Extract content and analyze sentiment from URLs")
    parser.add_argument("url", help="URL to extract content from")
    parser.add_argument("-l", "--language", help="Preferred language code for YouTube transcripts (e.g., 'en', 'es')")
    parser.add_argument("--raw", action="store_true", help="Output raw data (JSON)")
    parser.add_argument("--api", default="http://localhost:8000", help="API server URL")
    parser.add_argument("-o", "--output", help="Output file (default: print to stdout)")
    parser.add_argument("--sentiment", action="store_true", help="Perform sentiment analysis on the transcript")
    parser.add_argument("--top", type=int, default=5, help="Number of top positive/negative sentences to show")
    
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
                transcript_text = result.get("text", "No transcript available")
                output = transcript_text
                
                # Perform sentiment analysis if requested
                if args.sentiment and transcript_text != "No transcript available":
                    sentiment_results = analyze_sentiment(transcript_text, args.top)
                    sentiment_output = format_sentiment_results(sentiment_results)
                    output += sentiment_output
                    
                    # Add sentiment results to the result dict for raw output
                    if args.raw:
                        result["sentiment_analysis"] = sentiment_results
                        output = json.dumps(result, indent=2)
            else:
                # Format web page content
                title = result.get("title", "No title")
                text = result.get("text", "No content available")
                output = f"Title: {title}\n\n{text}"
                
                # Perform sentiment analysis if requested
                if args.sentiment and text != "No content available":
                    sentiment_results = analyze_sentiment(text, args.top)
                    sentiment_output = format_sentiment_results(sentiment_results)
                    output += sentiment_output
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

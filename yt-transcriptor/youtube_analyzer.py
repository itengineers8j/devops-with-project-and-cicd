#!/usr/bin/env python3
"""
Content Analyzer - Interactive menu-driven program for analyzing content from YouTube videos and web pages
"""
import os
import sys
import json
import re
import requests
from sentiment_analyzer import SentimentAnalyzer

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print application header"""
    print("\n" + "="*80)
    print("🔍 CONTENT EXTRACTION TOOL 🔍".center(80))
    print("="*80 + "\n")

def is_youtube_url(url):
    """Check if the URL is a YouTube URL"""
    youtube_patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&\s]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^\?\s]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^\?\s]+)'
    ]
    
    for pattern in youtube_patterns:
        if re.match(pattern, url):
            return True
    return False

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

def extract_quotes(text, top_n=5, sentiment_type='positive'):
    """Extract top positive or negative quotes from text"""
    analyzer = SentimentAnalyzer()
    quotes = analyzer.get_top_quotes(text, top_n, sentiment_type)
    return quotes

def format_quotes_output(quotes, sentiment_type='positive'):
    """Format quotes for display"""
    output = "\n" + "="*80 + "\n"
    output += f"TOP {len(quotes)} {sentiment_type.upper()} QUOTES\n"
    output += "="*80 + "\n\n"
    
    for i, item in enumerate(quotes, 1):
        output += f"{i}. {item['quote']} (Score: {item['score']:.3f})\n\n"
    
    return output

def save_to_file(content, filename):
    """Save content to a file"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Content saved to {filename}"
    except Exception as e:
        return f"Error saving to file: {str(e)}"

def get_language_choice():
    """Get language preference from user"""
    print("\n📋 Select language (leave blank for default):")
    print("1. English (en)")
    print("2. Spanish (es)")
    print("3. French (fr)")
    print("4. German (de)")
    print("5. Japanese (ja)")
    print("6. Korean (ko)")
    print("7. Other (specify code)")
    
    choice = input("\n👉 Enter choice (1-7) or press Enter for default: ")
    
    language_map = {
        "1": "en",
        "2": "es",
        "3": "fr",
        "4": "de",
        "5": "ja",
        "6": "ko"
    }
    
    if not choice:
        return None
    elif choice in language_map:
        return language_map[choice]
    elif choice == "7":
        return input("👉 Enter language code (e.g., ru, it, zh): ")
    else:
        print("❌ Invalid choice. Using default language.")
        return None

def display_youtube_menu(url, transcript_text):
    """Display interactive menu for working with YouTube transcripts"""
    while True:
        clear_screen()
        print_header()
        print(f"📺 YouTube Video: {url}\n")
        print("📋 Select an option:")
        print("1. View full transcript")
        print("2. Extract top positive quotes")
        print("3. Extract top negative quotes")
        print("4. Save transcript to file")
        print("5. Save quotes to file")
        print("6. Enter a new URL")
        print("7. Exit")
        
        choice = input("\n👉 Enter your choice (1-7): ")
        
        if choice == "1":
            clear_screen()
            print("\n📝 FULL TRANSCRIPT\n")
            print(transcript_text)
            input("\n👉 Press Enter to continue...")
            
        elif choice == "2":
            top_n = input("\n👉 How many quotes to extract? (default: 5): ")
            top_n = int(top_n) if top_n.isdigit() else 5
            
            quotes = extract_quotes(transcript_text, top_n, 'positive')
            
            clear_screen()
            print(format_quotes_output(quotes, 'positive'))
            input("\n👉 Press Enter to continue...")
            
        elif choice == "3":
            top_n = input("\n👉 How many quotes to extract? (default: 5): ")
            top_n = int(top_n) if top_n.isdigit() else 5
            
            quotes = extract_quotes(transcript_text, top_n, 'negative')
            
            clear_screen()
            print(format_quotes_output(quotes, 'negative'))
            input("\n👉 Press Enter to continue...")
            
        elif choice == "4":
            filename = input("\n👉 Enter filename to save transcript: ")
            if not filename:
                print("❌ No filename provided.")
                input("\n👉 Press Enter to continue...")
                continue
                
            result = save_to_file(transcript_text, filename)
            print(f"✅ {result}")
            input("\n👉 Press Enter to continue...")
            
        elif choice == "5":
            sentiment_type = input("\n👉 Extract which quotes? (positive/negative, default: positive): ").lower()
            if sentiment_type not in ["positive", "negative"]:
                sentiment_type = "positive"
                
            top_n = input("👉 How many quotes to extract? (default: 5): ")
            top_n = int(top_n) if top_n.isdigit() else 5
            
            quotes = extract_quotes(transcript_text, top_n, sentiment_type)
            formatted_quotes = format_quotes_output(quotes, sentiment_type)
            
            filename = input("👉 Enter filename to save quotes: ")
            if not filename:
                print("❌ No filename provided.")
                input("\n👉 Press Enter to continue...")
                continue
                
            result = save_to_file(formatted_quotes, filename)
            print(f"✅ {result}")
            input("\n👉 Press Enter to continue...")
            
        elif choice == "6":
            return True  # Signal to get a new URL
            
        elif choice == "7":
            print("\n👋 Thank you for using Content Extraction Tool. Goodbye!")
            return False  # Signal to exit
            
        else:
            print("\n❌ Invalid choice. Please try again.")
            input("\n👉 Press Enter to continue...")

def display_webpage_menu(url, title, content):
    """Display interactive menu for working with web page content"""
    while True:
        clear_screen()
        print_header()
        print(f"🌐 Web Page: {url}")
        print(f"📑 Title: {title}\n")
        print("📋 Select an option:")
        print("1. View full content")
        print("2. Extract top positive quotes")
        print("3. Extract top negative quotes")
        print("4. Save content to file")
        print("5. Save quotes to file")
        print("6. Enter a new URL")
        print("7. Exit")
        
        choice = input("\n👉 Enter your choice (1-7): ")
        
        if choice == "1":
            clear_screen()
            print(f"\n📝 {title}\n")
            print("="*80)
            print(content)
            input("\n👉 Press Enter to continue...")
            
        elif choice == "2":
            top_n = input("\n👉 How many quotes to extract? (default: 5): ")
            top_n = int(top_n) if top_n.isdigit() else 5
            
            quotes = extract_quotes(content, top_n, 'positive')
            
            clear_screen()
            print(format_quotes_output(quotes, 'positive'))
            input("\n👉 Press Enter to continue...")
            
        elif choice == "3":
            top_n = input("\n👉 How many quotes to extract? (default: 5): ")
            top_n = int(top_n) if top_n.isdigit() else 5
            
            quotes = extract_quotes(content, top_n, 'negative')
            
            clear_screen()
            print(format_quotes_output(quotes, 'negative'))
            input("\n👉 Press Enter to continue...")
            
        elif choice == "4":
            filename = input("\n👉 Enter filename to save content: ")
            if not filename:
                print("❌ No filename provided.")
                input("\n👉 Press Enter to continue...")
                continue
                
            formatted_content = f"{title}\n\n{content}"
            result = save_to_file(formatted_content, filename)
            print(f"✅ {result}")
            input("\n👉 Press Enter to continue...")
            
        elif choice == "5":
            sentiment_type = input("\n👉 Extract which quotes? (positive/negative, default: positive): ").lower()
            if sentiment_type not in ["positive", "negative"]:
                sentiment_type = "positive"
                
            top_n = input("👉 How many quotes to extract? (default: 5): ")
            top_n = int(top_n) if top_n.isdigit() else 5
            
            quotes = extract_quotes(content, top_n, sentiment_type)
            formatted_quotes = format_quotes_output(quotes, sentiment_type)
            
            filename = input("👉 Enter filename to save quotes: ")
            if not filename:
                print("❌ No filename provided.")
                input("\n👉 Press Enter to continue...")
                continue
                
            result = save_to_file(formatted_quotes, filename)
            print(f"✅ {result}")
            input("\n👉 Press Enter to continue...")
            
        elif choice == "6":
            return True  # Signal to get a new URL
            
        elif choice == "7":
            print("\n👋 Thank you for using Content Extraction Tool. Goodbye!")
            return False  # Signal to exit
            
        else:
            print("\n❌ Invalid choice. Please try again.")
            input("\n👉 Press Enter to continue...")

def main():
    """Main function"""
    while True:
        clear_screen()
        print_header()
        
        # Get URL
        print("Enter a URL to analyze:")
        print("- YouTube video URL (e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
        print("- Web page URL (e.g., https://example.com/article)")
        url = input("\n👉 Enter URL (or 'exit' to quit): ")
        
        if url.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Thank you for using Content Extraction Tool. Goodbye!")
            break
        
        # Detect URL type and handle accordingly
        is_youtube = is_youtube_url(url)
        
        if is_youtube:
            # Get language preference for YouTube videos
            language = get_language_choice()
            print("\n⏳ Fetching YouTube transcript... Please wait.")
        else:
            # Web page doesn't need language selection
            language = None
            print("\n⏳ Fetching web page content... Please wait.")
        
        # Extract content
        result = extract_content(url, language=language)
        
        if isinstance(result, dict):
            if result.get("content_type") == "youtube":
                transcript_text = result.get("text", "No transcript available")
                
                if transcript_text != "No transcript available":
                    # Show menu for working with the YouTube transcript
                    continue_program = display_youtube_menu(url, transcript_text)
                    if not continue_program:
                        break
                else:
                    print("\n❌ Error: No transcript available for this YouTube video.")
                    print("This could be because:")
                    print("- The video doesn't have captions")
                    print("- Captions are disabled by the creator")
                    print("- The selected language is not available")
                    input("\n👉 Press Enter to continue...")
            
            elif result.get("content_type") == "webpage":
                title = result.get("title", "No title")
                content = result.get("text", "No content available")
                
                if content != "No content available":
                    # Show menu for working with the web page content
                    continue_program = display_webpage_menu(url, title, content)
                    if not continue_program:
                        break
                else:
                    print("\n❌ Error: Could not extract content from this web page.")
                    input("\n👉 Press Enter to continue...")
            
            else:
                print(f"\n❌ Error: Unknown content type.")
                input("\n👉 Press Enter to continue...")
        else:
            print(f"\n❌ Error: {result if isinstance(result, str) else 'Failed to extract content'}")
            input("\n👉 Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted. Exiting...")
        sys.exit(0)

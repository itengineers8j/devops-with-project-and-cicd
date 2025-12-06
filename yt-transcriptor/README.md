# Content Extraction Tool

A Python application that extracts content from YouTube videos and web pages.

## Features

- Extract transcripts from YouTube videos using just the URL
- Extract text content from blogs, articles, and web pages
- Support for multiple YouTube URL formats (standard, short, embedded)
- Language selection for videos with multiple transcript options
- Formatted transcript output with timestamps
- Multiple web content extraction methods for best results
- **Sentiment analysis** of transcripts to identify positive and negative statements
- RESTful API with FastAPI
- Comprehensive test suite
- Command-line interface

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd youtube_transcript_app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   ```

## Usage

### Running the API server

```
python -m app.main
```

The API will be available at http://localhost:8000

### Docker Usage

You can also run the application using Docker:

#### Build and run with Docker

```
# Build the Docker image
docker build -t youtube-transcript-app .

# Run the container
docker run -p 8000:8000 youtube-transcript-app
```

#### Using Docker Compose

```
# Start the application
docker-compose up

# Run in background
docker-compose up -d
```

### API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints

#### Universal Endpoint

- `POST /content` - Automatically detects if the URL is a YouTube video or web page and extracts content accordingly
- `GET /content?url=<url>` - Same as above but using GET method

#### YouTube Specific

- `POST /transcript` - Extract transcript from a YouTube video URL
- `GET /transcript?url=<url>` - Same as above but using GET method

#### Web Page Specific

- `POST /webpage` - Extract content from a web page URL
- `GET /webpage?url=<url>` - Same as above but using GET method

### Command-line Usage

Extract content from any URL (YouTube or web page):

```
python client.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

Options:
- `-l, --language`: Specify language code for YouTube transcripts (e.g., "en", "es")
- `--raw`: Output raw data in JSON format
- `-o, --output`: Save output to a file
- `--api`: Specify custom API URL (default: http://localhost:8000)

Examples:
```
# Extract YouTube transcript in Spanish
python client.py https://www.youtube.com/watch?v=dQw4w9WgXcQ -l es

# Extract content from a blog post
python client.py https://example.com/blog/article

# Save output to a file
python client.py https://www.youtube.com/watch?v=dQw4w9WgXcQ -o transcript.txt
```

### Quote Extraction

Extract positive or negative quotes from YouTube videos or web pages:

```
python quote_extractor.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

Options:
- `--type`: Type of quotes to extract (`positive` or `negative`, default: positive)
- `--top`: Number of top quotes to show (default: 5)
- `--transcript-only`: Output only the transcript without sentiment analysis
- `-o, --output`: Save output to a file
- Other options same as client.py

Examples:
```
# Extract top 5 positive quotes
python quote_extractor.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --type positive

# Extract top 3 negative quotes
python quote_extractor.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --type negative --top 3

# Get only the transcript without sentiment analysis
python quote_extractor.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --transcript-only

# Save quotes to a file
python quote_extractor.py https://www.youtube.com/watch?v=dQw4w9WgXcQ -o quotes.txt
```

## Interactive Menu Interface

For a more user-friendly experience, you can use the interactive menu-driven interface:

```
python youtube_analyzer.py
```

This launches an interactive program that allows you to:
- Enter any URL (YouTube video or web page)
- Automatically detect content type and process accordingly
- Select language preference for YouTube videos
- View the full transcript or web page content
- Extract positive or negative quotes
- Save content or quotes to files
- Process multiple URLs in one session

The menu interface makes it easy to explore different analysis options without remembering command-line arguments.

## Web Content Extraction

The application uses multiple methods to extract content from web pages:

1. **Trafilatura** - Specialized in extracting main content from news articles and blogs
2. **Newspaper3k** - Extracts articles with additional metadata like authors and publish date
3. **BeautifulSoup** - Fallback method for general web page content extraction

The system automatically tries each method in order and uses the best result.

## Running Tests

```
pytest
```

## License

MIT

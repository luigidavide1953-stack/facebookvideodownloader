# Facebook Extractor

This project provides a robust API for extracting video information and download links from Facebook. It is built with FastAPI and leverages Playwright for web scraping, ensuring compatibility with various Facebook video formats including `fb.watch`, `share`, `watch`, `reel`, and `videos`.

## Features

- **FastAPI**: High-performance web framework for building APIs.
- **Public Facebook Link Extraction**: Supports extraction from various Facebook video URLs.
- **HTML Parser**: Utilizes BeautifulSoup for parsing HTML content.
- **Playwright (Headless Browser)**: Used as a fallback and primary extraction mechanism for dynamic content.
- **Caching**: Basic in-memory caching (can be extended with Redis).
- **Cookies Management**: Handles loading and potentially saving Facebook cookies for authenticated access.
- **REST API**: Provides a clean and structured API interface.
- **Docker Support**: Containerized for easy deployment and scalability.
- **Railway Deployment Ready**: Includes `railway.toml` for seamless deployment to Railway.
- **Swagger UI**: Automatic interactive API documentation.
- **Basic Tests**: Includes a basic test setup.

## Project Structure

```
facebook-extractor/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── services/
│   │   ├── cache.py
│   │   ├── cookies.py
│   │   ├── extractor.py
│   │   ├── graphql.py
│   │   ├── models.py
│   │   ├── parser.py
│   │   └── playwright.py
│   └── main.py
├── cookies/
│   └── facebook.txt
├── tests/
├── Dockerfile
├── docker-compose.yml
├── railway.toml
├── requirements.txt
├── README.md
└── .env.example
```

## Setup and Installation

### Prerequisites

- Python 3.10+
- Docker (optional, for containerized deployment)
- Note: The Docker image uses `mcr.microsoft.com/playwright/python` for optimal compatibility.

### Local Development

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository-url>
    cd facebook-extractor
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Install Playwright browsers:**
    ```bash
    playwright install chromium
    ```

4.  **Configure environment variables:**
    Copy the example environment file and modify it as needed:
    ```bash
    cp .env.example .env
    ```
    Edit `.env` to set `HEADLESS=false` if you want to see the browser actions during development.

5.  **Place Facebook cookies (optional):**
    If you need to extract from private or age-restricted content, place your Facebook cookies in `cookies/facebook.txt`. The format should be a JSON array of cookie objects, compatible with Playwright's `context.add_cookies()` method.

6.  **Run the application:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The API will be available at `http://localhost:8000` and the interactive documentation (Swagger UI) at `http://localhost:8000/docs`.

### Docker

1.  **Build and run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    This will start the FastAPI application and a Redis instance for caching. The API will be available at `http://localhost:8000`.

### Railway Deployment

This project includes a `railway.toml` file for easy deployment to Railway. Ensure your `Dockerfile` and `requirements.txt` are correctly configured. Railway will automatically detect the `railway.toml` and deploy the application.

## API Endpoints

-   **GET `/api/v1/extract?url=<facebook_video_url>`**
    Extracts metadata and available download links for a given Facebook video URL.
    -   **Parameters:**
        -   `url` (string, required): The URL of the Facebook video.
    -   **Responses:**
        -   `200 OK`: Returns `ExtractionResult` containing video metadata and formats.
        -   `400 Bad Request`: Returns `ErrorResponse` if the URL is invalid or extraction fails.

-   **GET `/api/v1/health`**
    Health check endpoint to verify the API is running.
    -   **Responses:**
        -   `200 OK`: Returns `{"status": "healthy"}`.

## Integration with `social-media-downloader-v2`

This `facebook-extractor` project is designed to be integrated directly into a larger social media downloader application. You can either run this as a separate service and call its API, or embed its core logic (services) directly into your `social-media-downloader-v2` project.

## Contributing

Feel free to fork the repository, open issues, or submit pull requests.

## License

This project is licensed under the MIT License.
